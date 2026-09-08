from __future__ import annotations

import os
import json
from uuid import uuid4

from ..rag.repository import RepositoryKnowledgeBase
from ..models import AnalysisResult, Classification, Event, Evidence, Source
from ..parsers.text import parse_log
from ..rules.engine import evaluate, rule_conclusion


class Analyzer:
    def __init__(self, knowledge: RepositoryKnowledgeBase) -> None:
        self.knowledge = knowledge

    def analyze(self, files: list[tuple[str, Source, str]], metadata: dict[str, str] | None = None) -> AnalysisResult:
        events: list[Event] = []
        for name, source, content in files:
            events.extend(parse_log(name, source, content))
        events.sort(key=lambda event: (event.timestamp is None, event.timestamp or event.line_number, event.file_name, event.line_number))
        scores, hits = evaluate(events)
        classification, confidence, summary, counter_evidence, actions = rule_conclusion(scores, hits)
        evidence = [evidence for hit in hits for evidence in hit.evidence][:8]
        query = " ".join(event.message for event in events if event.level in {"ERROR", "FATAL", "EXCEPTION", "WARN"})[:5000]
        knowledge_hits = self.knowledge.search(query)
        ai_status = "not_configured"
        model_version = "rules-v1"
        if os.getenv("OPENAI_API_KEY"):
            try:
                classification, confidence, summary, counter_evidence, actions = self._enhance_with_openai(
                    classification, confidence, summary, counter_evidence, actions, events, scores, hits, knowledge_hits
                )
                ai_status, model_version = "enhanced", os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            except Exception:
                # A provider failure must degrade safely to the evidence-backed
                # local result rather than making up an AI conclusion.
                ai_status = "provider_error_fallback"
        return AnalysisResult(
            analysis_id=str(uuid4()), metadata=metadata or {}, classification=classification, confidence=confidence,
            summary=summary, ai_status=ai_status, events=events, evidence=evidence,
            rule_hits=hits, scores=scores, knowledge_hits=knowledge_hits,
            counter_evidence=counter_evidence, recommended_actions=actions,
            model_version=model_version,
        )

    @staticmethod
    def _enhance_with_openai(classification, confidence, summary, counter_evidence, actions, events, scores, hits, knowledge_hits):
        from openai import OpenAI
        payload = {
            "rule_conclusion": classification.value, "rule_confidence": confidence, "scores": scores,
            "rules": [hit.model_dump(mode="json") for hit in hits],
            "events": [event.model_dump(mode="json", exclude={"raw"}) for event in events[-80:]],
            "knowledge": [hit.model_dump() for hit in knowledge_hits],
        }
        prompt = """你是 TraceJudge 的测试失败归因助手。只依据输入的日志事实、规则和知识库作推断；证据不足时必须返回 UNKNOWN。不要编造日志、文档、版本或修复事实。返回 JSON：classification（PRODUCT_DEVICE/TEST_TOOL/ENVIRONMENT/UNKNOWN）、confidence（0-1）、summary、counter_evidence（字符串数组）、recommended_actions（字符串数组）。"""
        response = OpenAI().chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": json.dumps(payload, ensure_ascii=False, default=str)}],
        )
        answer = json.loads(response.choices[0].message.content or "{}")
        selected = Classification(answer.get("classification", classification.value))
        value = float(answer.get("confidence", confidence))
        # The model cannot claim high confidence without a local evidence hit.
        if selected != Classification.UNKNOWN and not hits:
            selected, value = Classification.UNKNOWN, min(value, 0.4)
        return selected, max(0.0, min(1.0, value)), str(answer.get("summary", summary)), list(answer.get("counter_evidence", counter_evidence)), list(answer.get("recommended_actions", actions))
