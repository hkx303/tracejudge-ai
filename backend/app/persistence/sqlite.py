from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

from ..models import AnalysisResult, ConfirmationRequest

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DB_PATH = DATA_DIR / "tracejudge.db"

TOKEN = re.compile(r"(?i)(authorization:\s*bearer\s+|token[=:]\s*)([^\s,]+)")
EMAIL = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"(?<!\d)1\d{10}(?!\d)")


def redact(text: str) -> str:
    text = TOKEN.sub(r"\1[REDACTED]", text)
    text = EMAIL.sub("[REDACTED_EMAIL]", text)
    return PHONE.sub("[REDACTED_PHONE]", text)


def connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS analyses (id TEXT PRIMARY KEY, result_json TEXT NOT NULL)")
    conn.execute("CREATE TABLE IF NOT EXISTS confirmations (analysis_id TEXT PRIMARY KEY, classification TEXT NOT NULL, root_cause TEXT NOT NULL, confirmed_by TEXT NOT NULL)")
    return conn


def save_analysis(result: AnalysisResult) -> None:
    payload = result.model_dump(mode="json")
    for event in payload["events"]:
        event["raw"] = redact(event["raw"])
        event["message"] = redact(event["message"])
    with connection() as conn:
        conn.execute("INSERT OR REPLACE INTO analyses(id, result_json) VALUES (?, ?)", (result.analysis_id, json.dumps(payload, ensure_ascii=False)))


def get_analysis(analysis_id: str) -> AnalysisResult | None:
    with connection() as conn:
        row = conn.execute("SELECT result_json FROM analyses WHERE id = ?", (analysis_id,)).fetchone()
    return AnalysisResult.model_validate_json(row[0]) if row else None


def save_confirmation(analysis_id: str, request: ConfirmationRequest) -> None:
    with connection() as conn:
        conn.execute("INSERT OR REPLACE INTO confirmations VALUES (?, ?, ?, ?)", (analysis_id, request.classification.value, request.actual_root_cause, request.confirmed_by))
