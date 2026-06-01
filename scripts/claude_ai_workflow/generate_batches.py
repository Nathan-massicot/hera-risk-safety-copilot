"""Generate the markdown batch prompts to paste into Claude.ai.

Each batch produces 5 dialogues covering 5 different (archetype × dimension-subset)
pairs. Two full passes over the 35 archetypes => 14 batches => ~70 dialogues.

Usage:
    uv run python scripts/claude_ai_workflow/generate_batches.py
        --n-batches 14 --dialogues-per-batch 5 --seed 1337
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.build_training_set import sample_dimensions  # noqa: E402

ARCHETYPES_PATH = REPO_ROOT / "data/training/archetypes.json"
TAXONOMY_PATH = REPO_ROOT / "data/taxonomy/hera_taxonomy.json"
BATCH_DIR = REPO_ROOT / "scripts/claude_ai_workflow/batches"


BATCH_TEMPLATE = """# Batch {n:02d}

Paste this entire batch into the Claude.ai project chat. Claude should reply
with a single JSON object `{{"dialogues": [...]}}` containing **{k} dialogues**.
Save Claude's reply (only the JSON) to `responses/batch_{n:02d}.json`.

---

Produce **{k} dialogues** for the following (archetype, dimensions) pairs.

For each dialogue:
- Use `metadata.archetype_id` = the id below.
- Use `metadata.covered_dimensions` = the dimension IDs from the list (you may add 1–2 adjacent if natural).
- Follow ALL quality rules from the project instructions.

{cases}

Now produce the JSON object with all {k} dialogues, in the same order.
"""


CASE_TEMPLATE = """### Dialogue {i} — `{aid}`

**Archetype.** {name} (`{category}`, uses_ai={uses_ai}, data_sensitivity={ds}, vulnerable_pop={vp}, markets={markets}).
**Description.** {description}

**Dimensions to cover ({ndim}).**
{dims}
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-batches", type=int, default=14)
    ap.add_argument("--dialogues-per-batch", type=int, default=5)
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args(argv)

    archetypes = json.loads(ARCHETYPES_PATH.read_text())
    taxonomy = json.loads(TAXONOMY_PATH.read_text())
    rng = random.Random(args.seed)

    # Build the slot list: archetype × dimension-subset
    slots: list[tuple[dict, list[dict]]] = []
    target = args.n_batches * args.dialogues_per_batch
    pool = archetypes * ((target // len(archetypes)) + 1)
    rng.shuffle(pool)
    for a in pool[:target]:
        dims = sample_dimensions(taxonomy, a, n_min=4, n_max=7, rng=rng)
        slots.append((a, dims))

    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    (BATCH_DIR.parent / "responses").mkdir(parents=True, exist_ok=True)

    for b in range(args.n_batches):
        cases_md = []
        for i in range(args.dialogues_per_batch):
            idx = b * args.dialogues_per_batch + i
            a, dims = slots[idx]
            dim_lines = "\n".join(
                f"- [{d['id']}] {d['name']}: {d.get('description', '').strip()[:140]}"
                for d in dims
            )
            cases_md.append(CASE_TEMPLATE.format(
                i=i + 1,
                aid=a["id"],
                name=a["name"],
                category=a["category"],
                uses_ai=a["uses_ai"],
                ds=a["data_sensitivity"],
                vp=a["vulnerable_pop"],
                markets=", ".join(a["target_markets"]),
                description=a["description"],
                ndim=len(dims),
                dims=dim_lines,
            ))
        out = BATCH_TEMPLATE.format(
            n=b + 1,
            k=args.dialogues_per_batch,
            cases="\n".join(cases_md),
        )
        (BATCH_DIR / f"batch_{b + 1:02d}.md").write_text(out, encoding="utf-8")
        print(f"  wrote batches/batch_{b + 1:02d}.md  ({args.dialogues_per_batch} cases)")

    print(f"\nDone. {args.n_batches} batches × {args.dialogues_per_batch} dialogues = "
          f"{args.n_batches * args.dialogues_per_batch} target dialogues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
