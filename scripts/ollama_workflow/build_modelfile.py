"""Render Modelfile.template with the actual gguf filename + git sha + base model id."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE = REPO_ROOT / "scripts/ollama_workflow/Modelfile.template"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged-dir", type=Path, required=True,
                    help="Directory containing the gguf + training_state.json")
    ap.add_argument("--gguf-name", default="hera-baseline.q4_K_M.gguf",
                    help="Filename of the quantized gguf (relative to --merged-dir)")
    ap.add_argument("--out", type=Path, default=None,
                    help="Where to write the rendered Modelfile (default: <merged-dir>/Modelfile)")
    args = ap.parse_args(argv)

    state_path = args.merged_dir / "training_state.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        base_id = state.get("base_model_hf_id", "<unknown>")
        sha = state.get("git_sha", "<unknown>")
    else:
        base_id = "<unknown>"
        sha = "<unknown>"

    template = TEMPLATE.read_text(encoding="utf-8")
    rendered = (
        template
        .replace("{GGUF_FILENAME}", args.gguf_name)
        .replace("{BASE_MODEL_HF_ID}", base_id)
        .replace("{GIT_SHA}", sha[:7])
    )
    out = args.out or (args.merged_dir / "Modelfile")
    out.write_text(rendered, encoding="utf-8")
    print(f"Wrote {out}")
    print()
    print("Next: import into Ollama")
    print(f"  cd {args.merged_dir}")
    print(f"  ollama create hera-baseline -f Modelfile")
    print(f"  ollama run hera-baseline 'I am building a teleconsultation app.'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
