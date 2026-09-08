from __future__ import annotations

import re
from datetime import datetime
from uuid import uuid4

from ..models import Event, Source

TIMESTAMP = re.compile(r"(?:\[)?(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d{1,6})?(?:Z|[+-]\d{2}:?\d{2})?)(?:\])?")
LEVEL = re.compile(r"\b(DEBUG|INFO|WARN(?:ING)?|ERROR|FATAL|EXCEPTION)\b", re.I)
ERROR_CODE = re.compile(r"\b(?:code|error_code|errno)[=: ]+([A-Z][A-Z0-9_-]{2,})\b", re.I)
IDENTIFIERS = {
    "trace_id": re.compile(r"\btrace(?:_|-)?id[=: ]+([\w-]+)", re.I),
    "request_id": re.compile(r"\brequest(?:_|-)?id[=: ]+([\w-]+)", re.I),
    "session_id": re.compile(r"\bsession(?:_|-)?id[=: ]+([\w-]+)", re.I),
    "device_id": re.compile(r"\bdevice(?:_|-)?id[=: ]+([\w-]+)", re.I),
}


def _timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00").replace(",", "."))
    except ValueError:
        return None


def parse_log(file_name: str, source: Source, content: str) -> list[Event]:
    events: list[Event] = []
    for number, raw in enumerate(content.splitlines(), start=1):
        if not raw.strip():
            continue
        timestamp_match = TIMESTAMP.search(raw)
        level_match = LEVEL.search(raw)
        code_match = ERROR_CODE.search(raw)
        identifiers = {name: (match.group(1) if (match := pattern.search(raw)) else None) for name, pattern in IDENTIFIERS.items()}
        events.append(Event(
            event_id=str(uuid4()), file_name=file_name, source=source, line_number=number,
            raw=raw, timestamp=_timestamp(timestamp_match.group(1)) if timestamp_match else None,
            level=level_match.group(1).upper() if level_match else "INFO", message=raw,
            error_code=code_match.group(1) if code_match else None, **identifiers,
        ))
    return events
