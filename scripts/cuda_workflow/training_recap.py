"""Summarize the latest HERA fine-tune into a Markdown recap (losses, overfit check, adapter info)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def find_trainer_state() -> Path | None:
    cands = list((REPO / "models").rglob("trainer_state.json"))
    if not cands:
        return None

    def nlogs(p: Path) -> int:
        try:
            return len(json.loads(p.read_text()).get("log_history", []))
        except Exception:
            return -1

    return max(cands, key=nlogs)


def latest_run_dir() -> Path | None:
    runs = sorted((REPO / "runs").glob("finetune_*"))
    return runs[-1] if runs else None


def adapter_info():
    out = REPO / "models" / "baseline-lora"
    f = out / "adapter_model.safetensors"
    size = f.stat().st_size / 1e6 if f.exists() else None
    cfg = {}
    cf = out / "adapter_config.json"
    if cf.exists():
        try:
            cfg = json.loads(cf.read_text())
        except Exception:
            pass
    return size, cfg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    L: list[str] = ["# HERA fine-tune — training recap\n"]

    rd = latest_run_dir()
    if rd:
        L.append(f"- **Run**: `{rd.name}`")
        snap = rd / "training_config.yaml"
        if snap.exists():
            for line in snap.read_text().splitlines():
                if line.strip().startswith(("base_model", "seed")) or "max_seq_length" in line:
                    L.append(f"  - {line.strip()}")

    ts = find_trainer_state()
    if ts:
        st = json.loads(ts.read_text())
        logs = st.get("log_history", [])
        tr = [(l["step"], l["loss"]) for l in logs if "loss" in l]
        ev = [(l["step"], l["eval_loss"]) for l in logs if "eval_loss" in l]
        L.append(f"- **Steps**: {st.get('global_step')} | **epochs**: {round(st.get('epoch', 0), 2)}")
        if tr:
            L.append(f"- **Train loss**: {tr[0][1]:.3f} → {tr[-1][1]:.3f}")
        if ev:
            best_step, best = min(ev, key=lambda x: x[1])
            L.append(f"- **Eval loss**: {ev[0][1]:.3f} → {ev[-1][1]:.3f} (best **{best:.3f}** @ step {best_step})")
            if ev[-1][1] > best + 0.02:
                L.append("- ⚠️ **eval_loss remonte après le minimum → overfitting probable** (le meilleur checkpoint est conservé via load_best_model_at_end).")
            else:
                L.append("- ✅ eval_loss n'est pas reparti à la hausse → pas de signe net d'overfitting.")
        if tr:
            L.append("\n## Courbe train_loss\n| step | train_loss |\n|---:|---:|")
            L += [f"| {s} | {l:.4f} |" for s, l in tr]
        if ev:
            L.append("\n## Eval\n| step | eval_loss |\n|---:|---:|")
            L += [f"| {s} | {l:.4f} |" for s, l in ev]
    else:
        L.append("- ⚠️ Aucun `trainer_state.json` trouvé — l'entraînement n'a peut-être pas abouti.")

    size, acfg = adapter_info()
    if size:
        L.append(
            f"\n- **Adapter**: {size:.1f} MB · r={acfg.get('r')} α={acfg.get('lora_alpha')} "
            f"dropout={acfg.get('lora_dropout')} · targets={acfg.get('target_modules')}"
        )

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    print(f"\n→ écrit dans {out}")


if __name__ == "__main__":
    main()
