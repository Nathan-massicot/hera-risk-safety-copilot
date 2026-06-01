"""Parse Claude.ai batch responses and append valid dialogues to the training JSONL.

Reads every file under `scripts/claude_ai_workflow/responses/*.json`,
extracts the `dialogues` array (stripping ``` fences if present),
validates each dialogue against the training schema, and appends valid
ones to `data/training/conversations.jsonl`.

Idempotent: dialogues whose hash already exists in the output are skipped.
Run-level report is written to `runs/claude_import_<ts>/transcript.jsonl`.

Usage:
    uv run --extra datagen python scripts/claude_ai_workflow/import_batches.py
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_training_set import validate_example  # noqa: E402
from src.utils.logging_config import (  # noqa: E402
    JsonlSink,
    configure_logging,
    new_run_dir,
)

log = logging.getLogger("import")

RESPONSES_DIR = REPO_ROOT / "scripts/claude_ai_workflow/responses"
OUT_PATH = REPO_ROOT / "data/training/conversations.jsonl"

FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.DOTALL)


def strip_fences(text: str) -> str:
    text = text.strip()
    m = FENCE_RE.search(text)
    return m.group(1) if m else text


def dialogue_hash(example: dict) -> str:
    # Hash the first user+assistant turn — stable identifier for dedup
    msgs = example.get("messages", [])
    seed_text = ""
    for m in msgs:
        if m.get("role") in ("user", "assistant"):
            seed_text += m.get("content", "")[:500]
            if len(seed_text) > 500:
                break
    return hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:16]


def load_existing_hashes(path: Path) -> set[str]:
    if not path.exists():
        return set()
    seen: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            ex = json.loads(raw)
            seen.add(dialogue_hash(ex))
        except json.JSONDecodeError:
            continue
    return seen


def main() -> int:
    run_dir = new_run_dir(prefix="claude_import")
    configure_logging(run_dir)
    sink = JsonlSink(run_dir / "transcript.jsonl")

    if not RESPONSES_DIR.exists():
        log.error("Responses dir not found: %s", RESPONSES_DIR)
        log.error("Did you run generate_batches.py and paste any responses yet?")
        return 1

    files = sorted(RESPONSES_DIR.glob("batch_*.json"))
    if not files:
        log.warning("No batch_*.json files in %s — nothing to import.", RESPONSES_DIR)
        return 0

    seen = load_existing_hashes(OUT_PATH)
    log.info("Found %d existing dialogues in %s", len(seen), OUT_PATH.name)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    kept = 0
    duplicates = 0
    rejected = 0

    with OUT_PATH.open("a", encoding="utf-8") as out_fh:
        for fp in files:
            batch_name = fp.stem
            raw = fp.read_text(encoding="utf-8")
            try:
                payload = json.loads(strip_fences(raw))
            except json.JSONDecodeError as exc:
                log.warning("%s — JSON parse failed: %s", batch_name, exc)
                sink.write({"batch": batch_name, "event": "json_error", "error": str(exc)})
                rejected += 1
                continue

            dialogues = payload.get("dialogues") or (
                [payload] if "messages" in payload else []
            )
            if not dialogues:
                log.warning("%s — no `dialogues` array found", batch_name)
                rejected += 1
                continue

            for idx, ex in enumerate(dialogues):
                ex.setdefault("metadata", {})
                ex["metadata"].setdefault("source", "synthetic-claude-ai")
                ex["metadata"]["batch"] = batch_name
                ex["metadata"]["idx_in_batch"] = idx

                ok, msg = validate_example(ex)
                if not ok:
                    log.warning("%s#%d — schema fail: %s", batch_name, idx, msg)
                    sink.write({"batch": batch_name, "idx": idx, "event": "schema_error", "error": msg})
                    rejected += 1
                    continue

                h = dialogue_hash(ex)
                if h in seen:
                    duplicates += 1
                    sink.write({"batch": batch_name, "idx": idx, "event": "duplicate", "hash": h})
                    continue
                seen.add(h)

                out_fh.write(json.dumps(ex, ensure_ascii=False) + "\n")
                kept += 1
                sink.write({"batch": batch_name, "idx": idx, "event": "ok", "hash": h})

            log.info("processed %s — running totals: kept=%d duplicates=%d rejected=%d",
                     batch_name, kept, duplicates, rejected)

    sink.close()
    log.info("Done. kept=%d duplicates=%d rejected=%d → %s",
             kept, duplicates, rejected, OUT_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
