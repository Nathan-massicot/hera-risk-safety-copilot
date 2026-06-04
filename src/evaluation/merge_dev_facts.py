"""Merge bootstrapped developer fact sheets into scenarios.json.

Each `data/evaluation/_dev_facts/<id>.json` holds
`{"scenario_id": ..., "dev_facts": [{"dimension", "fact"}, ...]}` (produced by the
bootstrap workflow). This injects each `dev_facts` list into the matching scenario in
`scenarios.json` (idempotent — re-running replaces, never duplicates), backs up the
original, sanity-checks shape, and prints a coverage report.

    uv run python -m src.evaluation.merge_dev_facts
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCENARIOS = ROOT / "data/evaluation/scenarios.json"
FACTS_DIR = ROOT / "data/evaluation/_dev_facts"
DIM_RE = re.compile(r"^P\d\.D\d+$")


def load_facts() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for p in sorted(FACTS_DIR.glob("scenario_*.json")):
        if p.stem.startswith("_draft"):
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"  SKIP {p.name}: invalid JSON ({exc})")
            continue
        sid = d.get("scenario_id") or p.stem
        facts: list[dict] = []
        for f in d.get("dev_facts", []):
            dim = str(f.get("dimension", "")).strip()
            fact = str(f.get("fact", "")).strip()
            if not fact:
                continue
            if not DIM_RE.match(dim):
                print(f"  WARN {sid}: non-standard dimension {dim!r} kept as-is")
            facts.append({"dimension": dim, "fact": fact})
        out[sid] = facts
    return out


def main() -> int:
    scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    facts = load_facts()
    ids = {s["id"] for s in scenarios}

    missing = sorted(ids - set(facts))
    extra = sorted(set(facts) - ids)
    if missing:
        print("MISSING dev_facts for:", missing)
    if extra:
        print("EXTRA fact files ignored:", extra)
    if missing:
        print("\nRefusing to merge until all scenarios have dev_facts. Re-run the workflow.")
        return 1

    # Back up before mutating — but only the FIRST time, so re-running the merge can't
    # clobber the pristine pre-merge original with an already-merged copy.
    bak = SCENARIOS.with_suffix(".json.bak")
    if not bak.exists():
        bak.write_text(SCENARIOS.read_text(encoding="utf-8"), encoding="utf-8")

    injected = 0
    for s in scenarios:
        if s["id"] in facts:
            s["dev_facts"] = facts[s["id"]]
            injected += 1
    SCENARIOS.write_text(
        json.dumps(scenarios, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"injected dev_facts into {injected}/{len(scenarios)} scenarios; backup -> {bak.name}\n")

    print(f"{'scenario':14}{'sim_ans':>8}{'dev_facts':>10}{'pool':>6}{'gold_rel':>10}{'covered':>9}")
    tot_pool = 0
    for s in scenarios:
        sa = len(s.get("simulated_answers", {}))
        df = len(s.get("dev_facts", []))
        gold = set((s.get("gold_standard") or {}).get("relevant_dimensions") or [])
        fact_dims = {f["dimension"] for f in s.get("dev_facts", [])}
        tot_pool += sa + df
        print(f"  {s['id']:12}{sa:>8}{df:>10}{sa + df:>6}{len(gold):>10}{len(gold & fact_dims):>9}")
    print(f"\nmean pool size: {tot_pool / len(scenarios):.1f} facts/scenario")
    return 0


if __name__ == "__main__":
    sys.exit(main())
