"""Render the regulatory decision tree (accumulator model) into a standalone, shareable HTML.

Reads:  data/regulations/decision_tree_structure.json
Writes: data/regulations/decision_tree.html  (Mermaid flowchart + regulation legend, self-contained)

Also validates structural integrity (every `next`/`adds` target exists, every
question reachable, no dangling regulation) and prints a report. Exit code 1 if
the structure is broken — handy before sending the visual for verification.

Usage:
    uv run python scripts/render_decision_tree.py
    uv run python scripts/render_decision_tree.py --open   # also open in browser
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import webbrowser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TREE = REPO_ROOT / "data/regulations/decision_tree_structure.json"
OUT = REPO_ROOT / "data/regulations/decision_tree.html"

BRAND = "#FF6B1A"  # orange fluo HERA


def load() -> dict:
    return json.loads(TREE.read_text(encoding="utf-8"))


def validate(tree: dict) -> list[str]:
    """Return a list of structural problems (empty == valid)."""
    problems: list[str] = []
    q_ids = {q["id"] for q in tree["questions"]}
    exit_ids = {e["id"] for e in tree["exits"]}
    reg_ids = {r["id"] for r in tree["regulations"]}
    node_ids = q_ids | exit_ids

    if tree["start"] not in q_ids:
        problems.append(f"start '{tree['start']}' is not a question id")

    referenced_next: set[str] = set()
    used_regs: set[str] = set()
    for q in tree["questions"]:
        for a in q["answers"]:
            nxt = a["next"]
            referenced_next.add(nxt)
            if nxt not in node_ids:
                problems.append(f"{q['id']} answer '{a['value']}' -> unknown next '{nxt}'")
            for rid in a.get("adds", []):
                used_regs.add(rid)
                if rid not in reg_ids:
                    problems.append(f"{q['id']} answer '{a['value']}' adds unknown reg '{rid}'")

    # reachability from start (questions only; exits are sinks)
    reachable: set[str] = set()
    stack = [tree["start"]]
    while stack:
        nid = stack.pop()
        if nid in reachable or nid in exit_ids:
            continue
        reachable.add(nid)
        q = next((x for x in tree["questions"] if x["id"] == nid), None)
        if q:
            stack.extend(a["next"] for a in q["answers"])
    for qid in q_ids - reachable:
        problems.append(f"question '{qid}' is unreachable from start")

    for rid in reg_ids - used_regs:
        problems.append(f"regulation '{rid}' is never triggered by any answer")

    return problems


def mermaid(tree: dict) -> str:
    """Build a Mermaid flowchart definition string."""
    lines = ["flowchart TD"]
    # nodes
    for q in tree["questions"]:
        label = html.escape(f"{q['id']} · {q['text']}", quote=True).replace('"', "&quot;")
        lines.append(f'    {q["id"]}{{{{"{label}"}}}}')
    for e in tree["exits"]:
        # escape the two text parts separately, then join with a real <br/> (htmlLabels:true)
        label = f"{html.escape(e['id'])}<br/>{html.escape(e['title'])}".replace('"', "&quot;")
        shape = f'(["{label}"])' if e["type"] == "recap" else f'["{label}"]'
        lines.append(f"    {e['id']}{shape}")
    # edges
    reg_titles = {r["id"]: r["title"] for r in tree["regulations"]}
    for q in tree["questions"]:
        for a in q["answers"]:
            adds = a.get("adds", [])
            tag = " +" + ", ".join(reg_titles.get(r, r).split(" —")[0].split(" (")[0] for r in adds) if adds else ""
            edge_label = html.escape(f"{a['label']}{tag}").replace('"', "&quot;")
            lines.append(f'    {q["id"]} -->|"{edge_label}"| {a["next"]}')
    # styling
    lines.append(f"    classDef qnode fill:#ffffff,stroke:#9ca3af,stroke-width:1px,color:#111827;")
    lines.append(f"    classDef recap fill:{BRAND},stroke:{BRAND},color:#ffffff,font-weight:bold;")
    lines.append("    classDef out fill:#e5e7eb,stroke:#9ca3af,color:#374151;")
    qs = ",".join(q["id"] for q in tree["questions"])
    lines.append(f"    class {qs} qnode;")
    for e in tree["exits"]:
        lines.append(f"    class {e['id']} {'recap' if e['type'] == 'recap' else 'out'};")
    return "\n".join(lines)


def reg_table(tree: dict) -> str:
    rows = []
    for r in sorted(tree["regulations"], key=lambda x: x["id"]):
        arts = ", ".join(r.get("key_articles", []))
        rows.append(
            "<tr>"
            f"<td><code>{html.escape(r['id'])}</code></td>"
            f"<td><strong>{html.escape(r['title'])}</strong></td>"
            f"<td><span class='juris'>{html.escape(r['jurisdiction'])}</span></td>"
            f"<td>{html.escape(r['summary'])}</td>"
            f"<td class='arts'>{html.escape(arts)}</td>"
            f"<td><a href='{html.escape(r.get('official_url') or '#')}' target='_blank'>link</a></td>"
            "</tr>"
        )
    return "\n".join(rows)


def render(tree: dict, problems: list[str]) -> str:
    diagram = mermaid(tree)
    n_q = len(tree["questions"])
    n_reg = len(tree["regulations"])
    status = (
        "<span class='ok'>✓ consistent structure</span>"
        if not problems
        else "<span class='bad'>⚠ "
        + html.escape("; ".join(problems))
        + "</span>"
    )
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(tree['title'])}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
  :root {{ --brand: {BRAND}; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         margin: 0; color: #111827; background: #f9fafb; }}
  header {{ background: #ffffff; border-bottom: 3px solid var(--brand); padding: 20px 32px; }}
  header h1 {{ margin: 0 0 4px; font-size: 22px; }}
  header p {{ margin: 0; color: #6b7280; font-size: 14px; }}
  .meta {{ margin-top: 10px; font-size: 13px; color: #374151; }}
  .meta b {{ color: var(--brand); }}
  .ok {{ color: #15803d; font-weight: 600; }}
  .bad {{ color: #b91c1c; font-weight: 600; }}
  main {{ padding: 24px 32px 64px; }}
  section {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 12px;
            padding: 20px 24px; margin-bottom: 24px; }}
  h2 {{ font-size: 16px; margin: 0 0 16px; padding-bottom: 8px; border-bottom: 1px solid #f3f4f6; }}
  .mermaid {{ text-align: center; overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th, td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #f3f4f6; vertical-align: top; }}
  th {{ color: #6b7280; font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: .03em; }}
  code {{ background: #f3f4f6; padding: 1px 5px; border-radius: 4px; font-size: 12px; }}
  .juris {{ background: #fff1e8; color: var(--brand); border-radius: 999px; padding: 2px 8px; font-size: 11px; font-weight: 600; }}
  .arts {{ color: #6b7280; font-size: 12px; }}
  a {{ color: var(--brand); }}
</style>
</head>
<body>
<header>
  <h1>{html.escape(tree['title'])}</h1>
  <p>{html.escape(tree['subtitle'])}</p>
  <div class="meta">
    Version <b>{html.escape(tree['version'])}</b> · model <b>{html.escape(tree['model'])}</b>
    · {n_q} questions · {n_reg} regulations · {status}
  </div>
</header>
<main>
  <section>
    <h2>Decision tree</h2>
    <div class="mermaid">
{diagram}
    </div>
  </section>
  <section>
    <h2>Regulation cards ({n_reg}) — rich content to be written after validation</h2>
    <table>
      <thead><tr><th>id</th><th>Title</th><th>Jurisdiction</th><th>Summary</th><th>Key articles</th><th>Official</th></tr></thead>
      <tbody>
{reg_table(tree)}
      </tbody>
    </table>
  </section>
</main>
<script>
  mermaid.initialize({{ startOnLoad: true, theme: 'base',
    themeVariables: {{ primaryColor: '#ffffff', primaryBorderColor: '#9ca3af',
                      lineColor: '#9ca3af', fontSize: '13px' }},
    flowchart: {{ useMaxWidth: false, htmlLabels: true, nodeSpacing: 40, rankSpacing: 55 }} }});
</script>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--open", action="store_true", help="open the result in a browser")
    args = ap.parse_args(argv)

    tree = load()
    problems = validate(tree)
    OUT.write_text(render(tree, problems), encoding="utf-8")

    print(f"Wrote {OUT.relative_to(REPO_ROOT)}")
    print(f"  {len(tree['questions'])} questions · {len(tree['regulations'])} régulations · {len(tree['exits'])} exits")
    if problems:
        print("  STRUCTURE PROBLEMS:")
        for p in problems:
            print(f"    - {p}")
    else:
        print("  structure: OK (tous les liens et régulations sont cohérents)")

    if args.open:
        webbrowser.open(OUT.as_uri())
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
