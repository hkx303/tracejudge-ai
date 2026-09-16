from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..correlator.service import Analyzer
from ..models import ConfirmationRequest, Source
from ..persistence.sqlite import get_analysis, save_analysis, save_confirmation
from ..rag.repository import KB_ROOT, RepositoryKnowledgeBase

router = APIRouter(prefix="/api")
knowledge = RepositoryKnowledgeBase()
analyzer = Analyzer(knowledge)


@router.get("/health")
def health() -> dict[str, str | int]:
    return {"status": "ok", "knowledge_documents": len(knowledge.documents)}


@router.post("/analyses")
async def create_analysis(files: list[UploadFile] = File(...), sources: str = Form(...), metadata: str = Form("{}")):
    try:
        source_values = json.loads(sources)
    except json.JSONDecodeError:
        raise HTTPException(400, "sources must be a JSON array / sources 必须是 JSON 数组")
    if not isinstance(source_values, list) or len(files) != len(source_values):
        raise HTTPException(400, "Each file needs a source label / 每个文件必须提供一个来源标记")
    parsed: list[tuple[str, Source, str]] = []
    for upload, source in zip(files, source_values):
        suffix = Path(upload.filename or "").suffix.lower()
        if suffix not in {".log", ".txt"}:
            raise HTTPException(400, f"Unsupported file type / 不支持文件类型：{suffix or 'no extension / 无扩展名'}")
        try:
            parsed_source = Source(source)
        except ValueError:
            raise HTTPException(400, f"Unknown log source / 未知日志来源：{source}")
        parsed.append((upload.filename or "unknown.log", parsed_source, (await upload.read()).decode("utf-8", errors="replace")))
    try:
        decoded_metadata = json.loads(metadata)
        if not isinstance(decoded_metadata, dict):
            raise ValueError
        parsed_metadata = {str(key): str(value) for key, value in decoded_metadata.items()}
    except (json.JSONDecodeError, ValueError):
        raise HTTPException(400, "metadata must be a JSON object / metadata 必须是 JSON 对象")
    result = analyzer.analyze(parsed, parsed_metadata)
    save_analysis(result)
    return result


@router.get("/analyses/{analysis_id}")
def read_analysis(analysis_id: str):
    result = get_analysis(analysis_id)
    if not result:
        raise HTTPException(404, "Analysis not found / 未找到该分析任务")
    return result


@router.post("/analyses/{analysis_id}/confirmation")
def confirm_analysis(analysis_id: str, request: ConfirmationRequest):
    if not get_analysis(analysis_id):
        raise HTTPException(404, "Analysis not found / 未找到该分析任务")
    save_confirmation(analysis_id, request)
    cases = KB_ROOT / "cases"
    cases.mkdir(exist_ok=True)
    case_path = cases / f"{analysis_id}.md"
    case_path.write_text(f"# Verified case / 已确认案例 {analysis_id}\n\nverified: true\n\n- Classification / 归因：{request.classification.value}\n- Root cause / 根因：{request.actual_root_cause}\n- Confirmed by / 确认人：{request.confirmed_by}\n", encoding="utf-8")
    knowledge.reindex()
    return {"status": "saved", "case_path": str(case_path.relative_to(Path(__file__).resolve().parents[3]))}


@router.post("/knowledge/reindex")
def reindex_knowledge():
    return {"documents": knowledge.reindex()}
