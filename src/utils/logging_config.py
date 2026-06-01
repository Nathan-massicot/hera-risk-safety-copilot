"""Structured logging and per-run JSONL transcript persistence.

Each run gets a timestamped directory under `runs/<ts>/` containing:
- `run.log`         human-readable log
- `transcript.jsonl` one JSON object per conversation turn (or eval event)
- `config.yaml`     snapshot of the config used (written by the runner)
- `git.txt`         current git SHA (written by the runner)
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RUNS_DIR = REPO_ROOT / "runs"

_LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"


def new_run_dir(prefix: str = "run") -> Path:
    """Create a fresh `runs/<prefix>_<utc-ts>_<short-uuid>/` directory."""
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    short = uuid.uuid4().hex[:6]
    run_dir = RUNS_DIR / f"{prefix}_{ts}_{short}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def configure_logging(run_dir: Path | None = None, level: int = logging.INFO) -> Path:
    """Configure root logging to write both to stderr and `<run_dir>/run.log`.

    Returns the run directory (creates one if not provided).
    """
    if run_dir is None:
        run_dir = new_run_dir()

    log_file = run_dir / "run.log"
    formatter = logging.Formatter(_LOG_FORMAT)

    root = logging.getLogger()
    root.setLevel(level)
    # Wipe existing handlers to avoid duplicate lines on re-configure.
    root.handlers.clear()

    stream = logging.StreamHandler(sys.stderr)
    stream.setFormatter(formatter)
    root.addHandler(stream)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    logging.getLogger(__name__).info("Run directory: %s", run_dir)
    return run_dir


class JsonlSink:
    """Append-only JSONL writer for conversation transcripts or eval events."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self._path = path
        self._fh = path.open("a", encoding="utf-8")

    @property
    def path(self) -> Path:
        return self._path

    def write(self, event: dict) -> None:
        event.setdefault("ts", time.time())
        self._fh.write(json.dumps(event, ensure_ascii=False) + "\n")
        self._fh.flush()

    def close(self) -> None:
        self._fh.close()

    def __enter__(self) -> "JsonlSink":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


def load_dotenv(path: Path | str = ".env") -> dict[str, str]:
    """Minimal .env loader: KEY=VALUE per line, # comments, no shell expansion.

    Loaded values are pushed into os.environ unless already set.
    Returns the dict of values found.
    """
    p = Path(path)
    if not p.is_absolute():
        p = REPO_ROOT / p
    if not p.exists():
        return {}
    values: dict[str, str] = {}
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value
        os.environ.setdefault(key, value)
    return values
