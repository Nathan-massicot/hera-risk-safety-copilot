"""Render scenarios.json as a single Markdown document for human review.

Usage:
    uv run python scripts/render_scenarios.py
    # opens data/evaluation/scenarios.review.md
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "data/evaluation/scenarios.json"
OUT = REPO / "data/evaluation/scenarios.review.md"


def severity_emoji(s: str) -> str:
    return {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(s, "⚪")


def render(scenarios: list[dict]) -> str:
    parts: list[str] = [
        "# HERA Eval — 25 scenarios for review\n",
        f"_{len(scenarios)} scenarios · open `data/evaluation/scenarios.json` to edit_\n\n",
        "## How to review\n",
        "For each scenario, ask yourself:\n",
        "1. **App description plausible?** Could a real developer say this?\n",
        "2. **Gold-standard risks correct?** No invented regulations? Severities reasonable?\n",
        "3. **Mitigations actionable?** Could a dev actually implement them?\n",
        "4. **Coverage right?** Are the `relevant_dimensions` the ones a competent reviewer would cite?\n\n",
        "Flag issues in `scenarios_review_notes.md` (which I'll create alongside) — "
        "format: `scenario_NN: <what to change>`.\n\n---\n\n",
    ]
    for s in scenarios:
        meta = s["app_metadata"]
        gs = s["gold_standard"]
        parts.append(f"## {s['id']} — {meta['category']}\n\n")
        parts.append(
            f"**AI:** {meta['uses_ai']} · "
            f"**Sensitivity:** {meta['data_sensitivity']} · "
            f"**Vulnerable pop:** {meta['vulnerable_pop']} · "
            f"**Markets:** {', '.join(meta['target_markets'])} · "
            f"**Likely class:** {meta.get('samd_class_likely', 'n/a')}\n\n"
        )
        parts.append(f"### App description\n> {s['app_description']}\n\n")
        if s.get("developer_persona"):
            parts.append(f"_Persona: {s['developer_persona']}_\n\n")
        parts.append(
            f"**Relevant dimensions ({len(gs['relevant_dimensions'])}):** "
            f"`{'`, `'.join(gs['relevant_dimensions'])}`\n\n"
        )
        parts.append("### Expected risks\n\n")
        parts.append("| Sev | Dim | Risk |\n|---|---|---|\n")
        for r in gs["expected_risks"]:
            risk = r["risk"].replace("|", "\\|").replace("\n", " ")
            parts.append(f"| {severity_emoji(r['severity'])} {r['severity']} | `{r['dimension']}` | {risk} |\n")
        parts.append("\n")
        if gs.get("expected_mitigations"):
            parts.append("### Expected mitigations\n\n")
            for m in gs["expected_mitigations"]:
                miti = m["mitigation"].replace("\n", " ")
                parts.append(f"- `{m['dimension']}` — {miti}\n")
            parts.append("\n")
        if gs.get("expected_regulations_cited"):
            parts.append(
                f"**Expected regulations cited:** "
                f"{', '.join(gs['expected_regulations_cited'])}\n\n"
            )
        if s.get("notes"):
            parts.append(f"_Author notes: {s['notes']}_\n\n")
        parts.append("---\n\n")
    return "".join(parts)


def main() -> int:
    scenarios = json.loads(SRC.read_text(encoding="utf-8"))
    OUT.write_text(render(scenarios), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO)}  ({len(scenarios)} scenarios)")
    print(f"Open in your IDE: code {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
