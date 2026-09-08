from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field


class Source(StrEnum):
    TEST_TOOL = "test_tool"
    DEVICE = "device"
    PRODUCT_SERVICE = "product_service"
    ENVIRONMENT = "environment"


class Classification(StrEnum):
    PRODUCT_DEVICE = "PRODUCT_DEVICE"
    TEST_TOOL = "TEST_TOOL"
    ENVIRONMENT = "ENVIRONMENT"
    UNKNOWN = "UNKNOWN"


class Event(BaseModel):
    event_id: str
    file_name: str
    source: Source
    line_number: int
    raw: str
    timestamp: datetime | None = None
    level: str = "INFO"
    message: str
    error_code: str | None = None
    trace_id: str | None = None
    request_id: str | None = None
    session_id: str | None = None
    device_id: str | None = None


class Evidence(BaseModel):
    file_name: str
    line_number: int
    source: Source
    detail: str
    timestamp: datetime | None = None


class RuleHit(BaseModel):
    rule_id: str
    classification: Classification
    weight: float
    explanation: str
    evidence: list[Evidence] = Field(default_factory=list)


class KnowledgeHit(BaseModel):
    document_id: str
    path: str
    title: str
    excerpt: str
    score: float
    verified_case: bool = False


class AnalysisResult(BaseModel):
    analysis_id: str
    metadata: dict[str, str] = Field(default_factory=dict)
    classification: Classification
    confidence: float
    summary: str
    ai_status: str
    events: list[Event]
    evidence: list[Evidence]
    rule_hits: list[RuleHit]
    scores: dict[str, float]
    knowledge_hits: list[KnowledgeHit]
    counter_evidence: list[str]
    recommended_actions: list[str]
    needs_human_review: bool = True
    model_version: str = "rules-v1"
    prompt_version: str = "tracejudge-v1"
    knowledge_base_version: str = "repository-markdown-v1"


class ConfirmationRequest(BaseModel):
    classification: Classification
    actual_root_cause: str = Field(min_length=3, max_length=1000)
    confirmed_by: str = Field(default="anonymous", max_length=100)
