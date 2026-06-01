"""Render the regulatory decision tree (accumulator model) as a standalone INTERACTIVE walkthrough.

Reads:  data/regulations/decision_tree_structure.json
Writes: data/regulations/decision_tree_interactive.html  (self-contained: HTML + CSS + JS, tree embedded)

Unlike render_decision_tree.py (a static Mermaid diagram), this produces a clickable
questionnaire: the user answers one question at a time, applicable regulation cards
stack in a live side panel, and a final recap lists every triggered card. Back and
restart are supported. The whole tree JSON is embedded so the file works offline and
can be shared as a single .html.

Validates the structure first (same checks as the static renderer); exit code 1 if broken.

Usage:
    uv run python scripts/render_interactive_tree.py
    uv run python scripts/render_interactive_tree.py --open   # also open in browser
"""

from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TREE = REPO_ROOT / "data/regulations/decision_tree_structure.json"
OUT = REPO_ROOT / "data/regulations/decision_tree_interactive.html"

BRAND = "#FF6B1A"  # HERA orange fluo


def load() -> dict:
    return json.loads(TREE.read_text(encoding="utf-8"))


def _strip_frontmatter(text: str) -> str:
    """Remove a leading YAML frontmatter block (--- ... ---) and return the body."""
    if text.startswith("---"):
        idx = text.find("\n---", 3)
        if idx != -1:
            nl = text.find("\n", idx + 1)
            if nl != -1:
                return text[nl + 1:].lstrip("\n")
    return text


def load_rich() -> dict:
    """Load the rich Markdown cards (frontmatter stripped) keyed by id."""
    out: dict[str, str] = {}
    rich_dir = REPO_ROOT / "data/regulations/cards_rich"
    if not rich_dir.exists():
        return out
    for p in sorted(rich_dir.glob("*.md")):
        out[p.stem] = _strip_frontmatter(p.read_text(encoding="utf-8"))
    return out


def validate(tree: dict) -> list[str]:
    """Return a list of structural problems (empty == valid). Mirrors the static renderer."""
    problems: list[str] = []
    q_ids = {q["id"] for q in tree["questions"]}
    exit_ids = {e["id"] for e in tree["exits"]}
    reg_ids = {r["id"] for r in tree["regulations"]}
    node_ids = q_ids | exit_ids

    if tree["start"] not in q_ids:
        problems.append(f"start '{tree['start']}' is not a question id")

    used_regs: set[str] = set()
    for q in tree["questions"]:
        for a in q["answers"]:
            nxt = a["next"]
            if nxt not in node_ids:
                problems.append(f"{q['id']} answer '{a['value']}' -> unknown next '{nxt}'")
            for rid in a.get("adds", []):
                used_regs.add(rid)
                if rid not in reg_ids:
                    problems.append(f"{q['id']} answer '{a['value']}' adds unknown reg '{rid}'")

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


def render(tree: dict, rich: dict | None = None) -> str:
    data_json = json.dumps(tree, ensure_ascii=False).replace("</", "<\\/")
    rich_json = json.dumps(rich or {}, ensure_ascii=False).replace("</", "<\\/")
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>__TITLE__</title>
<style>
  :root { --brand: __BRAND__; --ink: #111827; --muted: #6b7280; --line: #e5e7eb; --bg: #f9fafb; }
  * { box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
         margin: 0; color: var(--ink); background: var(--bg); }
  header { background: #fff; border-bottom: 3px solid var(--brand); padding: 18px 32px; }
  header h1 { margin: 0 0 3px; font-size: 20px; }
  header p { margin: 0; color: var(--muted); font-size: 13px; }
  .wrap { display: grid; grid-template-columns: 1fr 380px; gap: 24px; padding: 24px 32px 64px;
          align-items: start; max-width: 1280px; margin: 0 auto; }
  @media (max-width: 900px) { .wrap { grid-template-columns: 1fr; } }
  .card { background: #fff; border: 1px solid var(--line); border-radius: 14px; padding: 24px; }

  /* progress */
  .progress { display: flex; align-items: center; gap: 10px; margin-bottom: 18px; font-size: 12px; color: var(--muted); }
  .bar { flex: 1; height: 6px; background: #f1f1f4; border-radius: 999px; overflow: hidden; }
  .bar > i { display: block; height: 100%; width: 0; background: var(--brand); transition: width .3s ease; }

  .qmeta { font-size: 12px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--brand); }
  .qtext { font-size: 21px; line-height: 1.35; margin: 8px 0 6px; }
  .qrat { font-size: 13px; color: var(--muted); line-height: 1.5; margin: 0 0 22px;
          border-left: 3px solid var(--line); padding-left: 12px; }
  .answers { display: flex; flex-direction: column; gap: 10px; }
  button.ans { text-align: left; cursor: pointer; border: 1.5px solid var(--line); background: #fff;
               border-radius: 10px; padding: 14px 16px; font-size: 15px; color: var(--ink);
               transition: all .15s ease; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
  button.ans:hover { border-color: var(--brand); background: #fff7f2; transform: translateY(-1px); }
  button.ans .tag { font-size: 11px; color: var(--brand); background: #fff1e8; border-radius: 999px;
                    padding: 3px 9px; white-space: nowrap; font-weight: 600; }
  .nav { margin-top: 22px; display: flex; gap: 12px; }
  .nav button { cursor: pointer; border: none; background: transparent; color: var(--muted);
                font-size: 13px; padding: 8px 4px; }
  .nav button:hover { color: var(--ink); }
  .nav button:disabled { opacity: .35; cursor: default; }

  /* side panel */
  .panel h2 { font-size: 13px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted);
              margin: 0 0 4px; }
  .panel .count { font-size: 12px; color: var(--brand); font-weight: 700; margin-bottom: 14px; }
  .reg { border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; margin-bottom: 10px;
         animation: pop .3s ease; }
  @keyframes pop { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
  .reg .rt { font-size: 14px; font-weight: 700; line-height: 1.3; }
  .reg .rj { font-size: 10px; color: var(--brand); background: #fff1e8; border-radius: 999px;
             padding: 2px 8px; font-weight: 700; margin-left: 6px; }
  .reg .rs { font-size: 12px; color: var(--muted); line-height: 1.5; margin: 7px 0 0; }
  .reg .ra { font-size: 11px; color: #9ca3af; margin-top: 7px; }
  .reg a { color: var(--brand); font-size: 12px; text-decoration: none; }
  .reg a:hover { text-decoration: underline; }
  .empty { font-size: 13px; color: #9ca3af; font-style: italic; }
  .reg.oos { opacity: .6; background: #fafafa; border-style: dashed; }
  .oosnote { font-size: 11px; color: #b45309; background: #fff7ed; border: 1px solid #fed7aa;
             border-radius: 6px; padding: 4px 8px; margin: 6px 0; line-height: 1.4; }
  .oossub { color: #9ca3af; font-weight: 500; }

  /* multi-select */
  button.ans.sel { border-color: var(--brand); background: #fff7f2; }
  button.ans .chk { width: 18px; height: 18px; border-radius: 5px; border: 1.5px solid #cbd5e1;
                    display: inline-flex; align-items: center; justify-content: center; font-size: 12px;
                    color: #fff; flex: 0 0 auto; }
  button.ans.sel .chk { background: var(--brand); border-color: var(--brand); }
  .continue { cursor: pointer; border: none; background: var(--brand); color: #fff; font-weight: 600;
              border-radius: 10px; padding: 12px 22px; font-size: 14px; margin-top: 16px; }
  .continue:hover { filter: brightness(.95); }
  .multihint { font-size: 12px; color: var(--muted); margin: -8px 0 14px; }

  /* rich card */
  .rcbtn { display: inline-block; margin-top: 8px; cursor: pointer; border: none; background: transparent;
           color: var(--brand); font-size: 12px; font-weight: 600; padding: 2px 0; }
  .rcbtn:hover { text-decoration: underline; }
  .richbox { margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--line); font-size: 13px;
             line-height: 1.55; color: #374151; }
  .richbox h4 { font-size: 12px; text-transform: uppercase; letter-spacing: .03em; color: var(--brand);
                margin: 14px 0 4px; }
  .richbox p { margin: 6px 0; }
  .richbox ul { margin: 6px 0; padding-left: 18px; }
  .richbox ul.md-check { list-style: none; padding-left: 2px; }
  .richbox ul.md-check li { margin: 3px 0; }
  .richbox code { background: #f3f4f6; padding: 1px 5px; border-radius: 4px; font-size: 12px; }
  .richbox a { color: var(--brand); }
  .xlink { cursor: pointer; background: #fff1e8; color: var(--brand); border-radius: 999px;
           padding: 1px 8px; font-size: 11px; font-weight: 600; text-decoration: none; white-space: nowrap; }
  .xlink:hover { filter: brightness(.96); text-decoration: none; }

  /* overlay */
  .overlay-bg { position: fixed; inset: 0; background: rgba(17,24,39,.55); z-index: 50;
                display: flex; align-items: flex-start; justify-content: center; padding: 5vh 16px; overflow-y: auto; }
  .overlay-card { background: #fff; border-radius: 14px; max-width: 640px; width: 100%; padding: 28px 30px;
                  position: relative; box-shadow: 0 20px 60px rgba(0,0,0,.25); }
  #ovclose { position: absolute; top: 12px; right: 16px; border: none; background: transparent;
             font-size: 26px; line-height: 1; color: var(--muted); cursor: pointer; }
  #ovclose:hover { color: var(--ink); }
  .ovhead { margin-bottom: 4px; }
  .overlay-card .rt { font-size: 18px; font-weight: 700; }
  .overlay-card h4 { font-size: 12px; text-transform: uppercase; letter-spacing: .03em; color: var(--brand);
                     margin: 16px 0 4px; }
  .overlay-card p { font-size: 14px; line-height: 1.6; margin: 7px 0; }
  .overlay-card ul { font-size: 14px; line-height: 1.6; padding-left: 18px; }
  .overlay-card ul.md-check { list-style: none; padding-left: 2px; }
  .overlay-card a { color: var(--brand); }
  .overlay-card .xlink { font-size: 12px; }

  /* recap / exit */
  .recap h2 { font-size: 22px; margin: 0 0 6px; }
  .recap .sub { color: var(--muted); font-size: 14px; margin: 0 0 20px; line-height: 1.5; }
  .recap .grid { display: grid; gap: 12px; }
  .restart { cursor: pointer; border: none; background: var(--brand); color: #fff; font-weight: 600;
             border-radius: 10px; padding: 12px 20px; font-size: 14px; margin-top: 8px; }
  .restart:hover { filter: brightness(.95); }
  .pill { display: inline-block; font-size: 11px; font-weight: 700; border-radius: 999px;
          padding: 3px 10px; background: #fff1e8; color: var(--brand); }
  .breadcrumb { font-size: 11px; color: #9ca3af; margin-top: 18px; line-height: 1.8; }
  .breadcrumb b { color: var(--muted); }
</style>
</head>
<body>
<header>
  <h1>__TITLE__</h1>
  <p>__SUBTITLE__ · interactive walkthrough</p>
</header>
<div class="wrap">
  <div id="stage" class="card"></div>
  <aside id="panel" class="card panel"></aside>
</div>

<div id="overlay-bg" class="overlay-bg" style="display:none">
  <div class="overlay-card">
    <button id="ovclose" title="Close">&times;</button>
    <div id="overlay-body"></div>
  </div>
</div>

<script>
const TREE = __DATA__;
const RICH = __RICH__;
const Q = Object.fromEntries(TREE.questions.map(q => [q.id, q]));
const X = Object.fromEntries(TREE.exits.map(e => [e.id, e]));
const REG = Object.fromEntries(TREE.regulations.map(r => [r.id, r]));

let state = { current: TREE.start, history: [], added: [], jurisdiction: null };
// history entries: { node, answerLabel, addedIds: [...] }  (addedIds = regs newly added by that answer)
// jurisdiction = value chosen at Q1 (start): 'eu' | 'ch' | 'both' | 'none' | null

function esc(s){ return (s||"").replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

function activeRegs(){
  // ordered unique list of accumulated regulation ids
  const seen = new Set(), out = [];
  for (const id of state.added){ if(!seen.has(id)){ seen.add(id); out.push(id); } }
  return out;
}

// Territorial scope: an EU-only card does not bind a Switzerland-only app, and vice versa.
function inScope(id){
  const j = state.jurisdiction;
  if (!j || j === "both" || j === "none") return true;
  const cj = (REG[id]||{}).jurisdiction;
  if (j === "eu") return cj !== "CH";
  if (j === "ch") return !(cj === "EU" || cj === "FR" || cj === "DE");
  return true;
}

// --- minimal Markdown renderer for the rich cards ---------------------------
function mdInline(s){
  s = esc(s);
  s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
  s = s.replace(/\[\[([a-z0-9_]+)\]\]/gi, (m,id) =>
    `<a class="xlink" data-card="${id}">${REG[id] ? esc(REG[id].title.split(" —")[0].split(" (")[0]) : id}</a>`);
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
  // auto-link bare URLs (not already inside an href="..."), trimming trailing punctuation
  s = s.replace(/(^|[^"'=>])(https?:\/\/[^\s<)]+)/g, (m, pre, url) => {
    let tail = "";
    while (/[.,;:]$/.test(url)){ tail = url.slice(-1) + tail; url = url.slice(0, -1); }
    return `${pre}<a href="${url}" target="_blank">${url}</a>${tail}`;
  });
  return s;
}
function mdToHtml(md){
  const lines = (md||"").split("\n");
  let html = "", inList = false;
  const closeList = () => { if (inList){ html += "</ul>"; inList = false; } };
  for (const raw of lines){
    const line = raw.replace(/\s+$/, "");
    if (!line.trim()){ closeList(); continue; }
    let m;
    if (/^#\s+/.test(line)){ closeList(); continue; } // skip H1 (title shown already)
    if (/^##\s+/.test(line)){ closeList(); html += `<h4>${mdInline(line.replace(/^##\s+/, ""))}</h4>`; continue; }
    if (m = line.match(/^- \[( |x|X)\]\s+(.*)/)){
      if (!inList){ html += '<ul class="md-check">'; inList = true; }
      html += `<li>${m[1].trim() ? "&#9745;" : "&#9744;"} ${mdInline(m[2])}</li>`; continue;
    }
    if (m = line.match(/^[-*]\s+(.*)/)){
      if (!inList){ html += "<ul>"; inList = true; }
      html += `<li>${mdInline(m[1])}</li>`; continue;
    }
    closeList(); html += `<p>${mdInline(line)}</p>`;
  }
  closeList();
  return html;
}
function toggleRich(id, btn){
  const box = document.getElementById("rc-" + id);
  if (!box) return;
  if (box.dataset.loaded !== "1"){ box.innerHTML = mdToHtml(RICH[id]); box.dataset.loaded = "1"; }
  const show = box.style.display === "none";
  box.style.display = show ? "block" : "none";
  if (btn) btn.innerHTML = "Read full card " + (show ? "&#9662;" : "&#9656;");
}
function openOverlay(id){
  const r = REG[id]; if (!r || !RICH[id]) return;
  document.getElementById("overlay-body").innerHTML =
    `<div class="ovhead"><span class="rt">${esc(r.title)}</span><span class="rj">${esc(r.jurisdiction)}</span></div>` + mdToHtml(RICH[id]);
  document.getElementById("overlay-bg").style.display = "flex";
}
function closeOverlay(){ document.getElementById("overlay-bg").style.display = "none"; }

document.addEventListener("click", (e) => {
  const btn = e.target.closest(".rcbtn");
  if (btn){ toggleRich(btn.dataset.card, btn); return; }
  const xl = e.target.closest(".xlink");
  if (xl){ openOverlay(xl.dataset.card); return; }
  if (e.target.id === "overlay-bg" || e.target.closest("#ovclose")){ closeOverlay(); return; }
});
document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeOverlay(); });

function regCard(id){
  const r = REG[id]; if(!r) return "";
  const arts = (r.key_articles||[]).join(" · ");
  const link = r.official_url ? `<a href="${esc(r.official_url)}" target="_blank">official source &rarr;</a>` : "";
  const oos = !inScope(id);
  const jurLabel = state.jurisdiction === "ch" ? "Switzerland" : "the EU";
  const note = oos ? `<div class="oosnote">Outside your territorial scope — does not bind ${jurLabel} directly (shown for reference)</div>` : "";
  const hasRich = !!RICH[id];
  const richUi = hasRich
    ? `<button class="rcbtn" data-card="${id}">Read full card &#9656;</button><div class="richbox" id="rc-${id}" style="display:none"></div>`
    : "";
  return `<div class="reg${oos ? " oos" : ""}">
    <div><span class="rt">${esc(r.title)}</span><span class="rj">${esc(r.jurisdiction)}</span></div>
    ${note}
    <p class="rs">${esc(r.summary)}</p>
    ${arts ? `<div class="ra">${esc(arts)}</div>` : ""}
    ${link}
    ${richUi}
  </div>`;
}

function renderPanel(){
  const regs = activeRegs();
  const inS = regs.filter(inScope), oos = regs.filter(id => !inScope(id));
  const panel = document.getElementById("panel");
  const sub = oos.length ? ` <span class="oossub">+ ${oos.length} out-of-scope (greyed)</span>` : "";
  panel.innerHTML = `<h2>Applicable regulations</h2>
    <div class="count">${inS.length} card${inS.length===1?"":"s"} triggered${sub}</div>
    ${regs.length ? regs.map(regCard).join("") : '<p class="empty">None yet — answer the questions and cards will stack here.</p>'}`;
}

function answeredCount(){ return state.history.length; }
function totalQuestions(){ return TREE.questions.length; }

function answerTag(a){
  const adds = (a.adds||[]).map(id => (REG[id]?REG[id].title.split(" —")[0].split(" (")[0]:id));
  return adds.length ? `<span class="tag">+ ${esc(adds.join(", "))}</span>` : "";
}

function renderQuestion(){
  const q = Q[state.current];
  const stage = document.getElementById("stage");
  const pct = Math.round(100 * answeredCount() / totalQuestions());
  const isGate = q.type === "gate";
  const multi = q.multiSelect === true;
  const meta = isGate ? " · gate" : (multi ? " · choose all that apply" : (q.type==="multichoice" ? " · choose one" : ""));
  state.multiSel = new Set();
  stage.innerHTML = `
    <div class="progress">
      <span>${answeredCount()} / ${totalQuestions()}</span>
      <span class="bar"><i style="width:${pct}%"></i></span>
      <span>${q.id}${isGate ? " · gate" : ""}</span>
    </div>
    <div class="qmeta">${esc(q.id)}${meta}</div>
    <div class="qtext">${esc(q.text)}</div>
    ${q.rationale ? `<p class="qrat">${esc(q.rationale)}</p>` : ""}
    ${multi ? `<p class="multihint">Tick every market/option that applies, then continue.</p>` : ""}
    <div class="answers">
      ${q.answers.map((a,i) =>
        `<button class="ans" data-i="${i}">${multi ? '<span class="chk">&#10003;</span>' : ""}<span>${esc(a.label)}</span>${answerTag(a)}</button>`
      ).join("")}
    </div>
    ${multi ? `<button class="continue" id="continue">Continue &rarr;</button>` : ""}
    <div class="nav">
      <button id="back" ${state.history.length?"":"disabled"}>&larr; Back</button>
      <button id="restart2">Restart</button>
    </div>`;
  if (multi){
    stage.querySelectorAll("button.ans").forEach(b => b.onclick = () => {
      const i = +b.dataset.i;
      if (state.multiSel.has(i)) state.multiSel.delete(i); else state.multiSel.add(i);
      b.classList.toggle("sel");
    });
    document.getElementById("continue").onclick = () => chooseMulti();
  } else {
    stage.querySelectorAll("button.ans").forEach(b => b.onclick = () => choose(+b.dataset.i));
  }
  document.getElementById("back").onclick = goBack;
  document.getElementById("restart2").onclick = restart;
}

function renderExit(){
  const e = X[state.current];
  const stage = document.getElementById("stage");
  const regs = activeRegs();
  const inS = regs.filter(inScope), oos = regs.filter(id => !inScope(id));
  let body = "";
  if (e.type === "recap"){
    if (!regs.length){
      body = `<p class="empty">No regulation was triggered along this path.</p>`;
    } else {
      body = `<div class="grid">${inS.map(regCard).join("")}</div>`;
      if (oos.length){
        body += `<p class="sub" style="margin-top:22px">Triggered but outside your territorial scope (${oos.length}) — shown for reference:</p>`;
        body += `<div class="grid">${oos.map(regCard).join("")}</div>`;
      }
    }
  }
  const crumbs = state.history.map(h => `<b>${esc(Q[h.node]?h.node:h.node)}</b> ${esc(h.answerLabel)}`).join("  ·  ");
  stage.innerHTML = `
    <div class="recap">
      <span class="pill">${e.type === "recap" ? "Summary" : "Exit"}</span>
      <h2>${esc(e.title)}</h2>
      <p class="sub">${esc(e.summary)}</p>
      ${e.type === "recap" ? `<p class="sub"><strong>${inS.length}</strong> regulation${inS.length===1?"":"s"} apply to your app${oos.length?` (+ ${oos.length} EU-only, not binding for your jurisdiction)`:""}.</p>` : ""}
      ${body}
      <div class="nav"><button id="back">&larr; Back</button></div>
      <br/><button class="restart" id="restart3">Start over</button>
      <div class="breadcrumb">${crumbs}</div>
    </div>`;
  document.getElementById("back").onclick = goBack;
  document.getElementById("restart3").onclick = restart;
}

function draw(){
  if (Q[state.current]) renderQuestion();
  else renderExit();
  renderPanel();
}

function commitStep(node, answerLabel, addedIds, next){
  if (node === TREE.start){
    // capture jurisdiction from the Q1 answer value
    const q = Q[node];
    const ans = q.answers.find(a => a.label === answerLabel.split(" + ")[0]) || q.answers[0];
    state.jurisdiction = ans ? ans.value : null;
  }
  state.history.push({ node, answerLabel, addedIds, setJurisdiction: node === TREE.start });
  state.added.push(...addedIds);
  state.current = next;
  draw();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function choose(i){
  const q = Q[state.current];
  const a = q.answers[i];
  commitStep(state.current, a.label, (a.adds||[]).slice(), a.next);
}

function chooseMulti(){
  const q = Q[state.current];
  const picked = [...state.multiSel].sort((x,y)=>x-y).map(i => q.answers[i]);
  const sel = picked.length ? picked : [q.answers[q.answers.length-1]]; // none ticked = last ("No") option
  const addedIds = [].concat(...sel.map(a => (a.adds||[]).slice()));
  const label = sel.map(a => a.label).join(" + ");
  const next = sel[0].next; // all options of a multi-select question share the same next
  commitStep(state.current, label, addedIds, next);
}

function goBack(){
  const last = state.history.pop();
  if (!last) return;
  // remove the regs that this step added
  for (const id of last.addedIds){
    const idx = state.added.lastIndexOf(id);
    if (idx !== -1) state.added.splice(idx, 1);
  }
  if (last.setJurisdiction) state.jurisdiction = null;
  state.current = last.node;
  draw();
}

function restart(){
  state = { current: TREE.start, history: [], added: [], jurisdiction: null };
  draw();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

draw();
</script>
</body>
</html>
""".replace("__TITLE__", _esc(tree["title"])).replace("__SUBTITLE__", _esc(tree["subtitle"])).replace("__BRAND__", BRAND).replace("__DATA__", data_json).replace("__RICH__", rich_json)


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--open", action="store_true", help="open the result in a browser")
    args = ap.parse_args(argv)

    tree = load()
    problems = validate(tree)
    if problems:
        print("STRUCTURE PROBLEMS (interactive HTML not written):")
        for p in problems:
            print(f"  - {p}")
        return 1

    rich = load_rich()
    OUT.write_text(render(tree, rich), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO_ROOT)}")
    print(f"  {len(tree['questions'])} questions · {len(tree['regulations'])} regulations · {len(rich)} rich cards · interactive walkthrough")

    if args.open:
        webbrowser.open(OUT.as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
