"""Persist conversation messages to per-user JSONL transcripts on disk."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from .config import settings

_SAFE_RE = re.compile(r"[^a-zA-Z0-9._-]+")


def _slug(value: str) -> str:
    return _SAFE_RE.sub("_", value).strip("_") or "user"


def transcript_path(user_email: str, conversation_id: int) -> Path:
    folder = settings.transcripts_dir / _slug(user_email)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"conversation_{conversation_id}.jsonl"


def append_turn(user_email: str, conversation_id: int, role: str, content: str) -> None:
    record = {
        "ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "role": role,
        "content": content,
    }
    with transcript_path(user_email, conversation_id).open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
