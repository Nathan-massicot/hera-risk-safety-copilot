"""Build manual (hand-written) dialogues from a dead-simple text format into the training JSONL.

Authoring format — `manual_dialogues.md`:
- One dialogue per block; blocks separated by a line containing only `===`.
- A block starts with `@archetype_id` (a short snake_case id).
- Then alternating `U:` (user) and `A:` (assistant) lines.
- A turn may span several lines: continuation lines (not starting with U:/A:/@/===)
  are appended to the current turn.
- Cite HERA dimensions in the ASSISTANT lines as `[P1.D2]` — they are auto-collected
  into `metadata.covered_dimensions`. No need to list them by hand.

The script injects the verbatim HERA system message, sets `source: "manual"`,
validates each dialogue against the training schema, dedups against the existing
JSONL, and appends the valid ones.

Usage:
    uv run --extra datagen python scripts/claude_ai_workflow/build_manual.py            # import
    uv run --extra datagen python scripts/claude_ai_workflow/build_manual.py --dry-run  # validate only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_training_set import validate_example  # noqa: E402

SRC = REPO_ROOT / "scripts/claude_ai_workflow/manual_dialogues.md"
OUT = REPO_ROOT / "data/training/conversations.jsonl"

SYSTEM = (
    "You are the HERA Risk & Safety Copilot. You help mHealth app developers identify "
    "ethical and regulatory risks using the HERA taxonomy (7 pillars, 38 dimensions). "
    "Ask targeted reflection questions one or two at a time, drill into specifics, "
    "surface concrete risks with their HERA dimension ID, and suggest actionable "
    "mitigations referencing relevant regulations (GDPR, MDR, EU AI Act, ISO 82304-2)."
)

VALID_DIMS = {
    f"P{p}.D{d}"
    for p, n in [(1, 6), (2, 6), (3, 5), (4, 5), (5, 4), (6, 5), (7, 7)]
    for d in range(1, n + 1)
}
DIM_RE = re.compile(r"\[?(P[1-7]\.D[1-9])\]?")


def dialogue_hash(ex: dict) -> str:
    seed = ""
    for m in ex.get("messages", []):
        if m.get("role") in ("user", "assistant"):
            seed += m.get("content", "")[:500]
            if len(seed) > 500:
                break
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def existing_hashes() -> set[str]:
    if not OUT.exists():
        return set()
    out = set()
    for line in OUT.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                out.add(dialogue_hash(json.loads(line)))
            except json.JSONDecodeError:
                pass
    return out


def parse_blocks(text: str) -> list[dict]:
    examples: list[dict] = []
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)  # drop HTML comments
    for raw_block in re.split(r"^\s*===\s*$", text, flags=re.MULTILINE):
        block = raw_block.strip()
        if not block or block.startswith("<!--"):
            continue
        archetype = None
        turns: list[tuple[str, str]] = []  # (role, content)
        for line in block.splitlines():
            s = line.rstrip()
            if not s.strip():
                continue
            if s.lstrip().startswith("@"):
                archetype = s.lstrip()[1:].strip()
            elif s.lstrip().startswith("U:"):
                turns.append(("user", s.split("U:", 1)[1].strip()))
            elif s.lstrip().startswith("A:"):
                turns.append(("assistant", s.split("A:", 1)[1].strip()))
            elif turns:  # continuation of the current turn
                role, content = turns[-1]
                turns[-1] = (role, (content + " " + s.strip()).strip())
        if not archetype or not turns:
            continue
        messages = [{"role": "system", "content": SYSTEM}]
        dims: list[str] = []
        for role, content in turns:
            messages.append({"role": role, "content": content})
            if role == "assistant":
                for m in DIM_RE.findall(content):
                    if m in VALID_DIMS and m not in dims:
                        dims.append(m)
        examples.append(
            {
                "messages": messages,
                "metadata": {
                    "archetype_id": archetype,
                    "covered_dimensions": dims,
                    "source": "manual",
                },
            }
        )
    return examples


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="validate only, do not write")
    args = ap.parse_args()

    if not SRC.exists():
        print(f"Not found: {SRC}")
        return 1

    examples = parse_blocks(SRC.read_text(encoding="utf-8"))
    print(f"Parsed {len(examples)} dialogue block(s) from {SRC.name}\n")

    seen = existing_hashes()
    ok_rows, kept, dup, bad = [], 0, 0, 0
    for ex in examples:
        a = ex["metadata"]["archetype_id"]
        nturns = len(ex["messages"])
        valid, msg = validate_example(ex)
        bad_dims = [d for d in ex["metadata"]["covered_dimensions"] if d not in VALID_DIMS]
        flags = []
        if not valid:
            flags.append(f"schema: {msg}")
        if not (9 <= nturns <= 15):
            flags.append(f"turns={nturns} (want 9-15)")
        if not ex["metadata"]["covered_dimensions"]:
            flags.append("no [Px.Dy] cited in assistant turns")
        if bad_dims:
            flags.append(f"bad dims {bad_dims}")
        if flags:
            print(f"  ✗ {a}: " + "; ".join(flags))
            bad += 1
            continue
        h = dialogue_hash(ex)
        if h in seen:
            print(f"  ~ {a}: duplicate, skipped")
            dup += 1
            continue
        seen.add(h)
        ok_rows.append(ex)
        print(f"  ✓ {a}: {nturns} msgs, dims {ex['metadata']['covered_dimensions']}")
        kept += 1

    print(f"\nvalid={kept}  duplicates={dup}  rejected={bad}")
    if args.dry_run:
        print("(dry-run — nothing written)")
        return 0
    if ok_rows:
        with OUT.open("a", encoding="utf-8") as fh:
            for ex in ok_rows:
                fh.write(json.dumps(ex, ensure_ascii=False) + "\n")
        print(f"Appended {len(ok_rows)} dialogues → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
