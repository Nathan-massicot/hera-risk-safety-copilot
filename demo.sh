#!/usr/bin/env bash
#
# HERA Copilot — one-command demo launcher.
#
# After `git clone`, a tester just runs:
#
#     ./demo.sh
#
# It installs everything, makes sure a local Ollama model is available
# (the LLM runs on *this* machine — no API keys, no remote endpoint),
# builds the web app, prints a ready-to-use invite token, and serves the
# whole thing on a single URL.
#
# Override the model with:  HERA_OLLAMA_MODEL=qwen3:4b ./demo.sh
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

MODEL="${HERA_OLLAMA_MODEL:-qwen3:8b}"
HOST="127.0.0.1"
PORT="${HERA_PORT:-8000}"
URL="http://${HOST}:${PORT}"

# ---- pretty output ---------------------------------------------------------
if [ -t 1 ]; then
  ORANGE='\033[1;38;5;208m'; GREEN='\033[32m'; RED='\033[31m'; DIM='\033[2m'; RST='\033[0m'
else
  ORANGE=''; GREEN=''; RED=''; DIM=''; RST=''
fi
step() { printf "\n${ORANGE}▶ %s${RST}\n" "$1"; }
ok()   { printf "  ${GREEN}✓${RST} %s\n" "$1"; }
info() { printf "  ${DIM}%s${RST}\n" "$1"; }
die()  { printf "\n${RED}✗ %s${RST}\n" "$1" >&2; exit 1; }

OS="$(uname -s)"
have() { command -v "$1" >/dev/null 2>&1; }

# Track whether *we* started Ollama, so we only clean up what we own.
OLLAMA_PID=""
cleanup() {
  if [ -n "$OLLAMA_PID" ] && kill -0 "$OLLAMA_PID" 2>/dev/null; then
    info "Stopping Ollama (pid $OLLAMA_PID)…"
    kill "$OLLAMA_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

# ---- 1. prerequisites ------------------------------------------------------
step "Checking prerequisites"

if ! have uv; then
  info "uv not found — installing (https://astral.sh/uv)…"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # shellcheck disable=SC1090
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
  have uv || die "uv install failed — install it manually: https://docs.astral.sh/uv/getting-started/installation/"
fi
ok "uv $(uv --version 2>/dev/null | awk '{print $2}')"

if ! have node || ! have npm; then
  if [ "$OS" = "Darwin" ] && have brew; then
    info "Node not found — installing via Homebrew…"
    brew install node
  fi
  have node && have npm || die "Node.js (with npm) is required. Install Node 18+ from https://nodejs.org and re-run."
fi
ok "node $(node --version)"

if ! have ollama; then
  if [ "$OS" = "Darwin" ] && have brew; then
    info "Ollama not found — installing via Homebrew…"
    brew install ollama
  elif [ "$OS" = "Linux" ]; then
    info "Ollama not found — installing (https://ollama.com)…"
    curl -fsSL https://ollama.com/install.sh | sh
  fi
  have ollama || die "Ollama is required. Install it from https://ollama.com/download and re-run."
fi
ok "ollama present"

# ---- 2. python + frontend deps --------------------------------------------
step "Installing backend dependencies (uv sync --extra web --extra rag)"
# 'rag' brings chromadb + sentence-transformers (pulls torch) — needed so the
# chatbot runs the retrieval-augmented config that won the eval, not a silent
# prompt-only fallback. First install is large (~1-2 GB); cached afterwards.
uv sync --extra web --extra rag
ok "Python environment ready"

step "Building the web frontend"
( cd web/frontend
  if [ -d node_modules ]; then
    info "node_modules present — skipping npm install (delete it to force a fresh install)"
  else
    npm install
  fi
  npm run build )
ok "Frontend built → web/frontend/dist"

# ---- 2b. RAG knowledge base ------------------------------------------------
# The Chroma index is git-ignored (it can contain copyrighted PDF text), so a
# fresh clone has none. Rebuild it from the committed regulatory cards — fully
# reproducible and copyright-safe. First run downloads the bge embedding model.
step "Preparing the RAG knowledge base (Chroma index)"
if [ -f models/chroma_hera/chroma.sqlite3 ]; then
  ok "Chroma index already present → models/chroma_hera"
else
  info "Building index from the curated regulatory cards (first run downloads the embedding model)…"
  uv run python -m src.rag.ingest --cards
  ok "RAG index built → models/chroma_hera"
fi

# ---- 3. local model --------------------------------------------------------
step "Starting Ollama and ensuring the model is available"
if curl -s -m 2 "http://localhost:11434/api/tags" >/dev/null 2>&1; then
  ok "Ollama already running"
else
  info "Launching 'ollama serve' in the background…"
  ollama serve >/tmp/hera-ollama.log 2>&1 &
  OLLAMA_PID=$!
  for _ in $(seq 1 60); do
    curl -s -m 2 "http://localhost:11434/api/tags" >/dev/null 2>&1 && break
    sleep 0.5
  done
  curl -s -m 2 "http://localhost:11434/api/tags" >/dev/null 2>&1 \
    || die "Ollama did not come up — see /tmp/hera-ollama.log"
  ok "Ollama started (pid $OLLAMA_PID)"
fi

if ollama list 2>/dev/null | awk '{print $1}' | grep -qx "$MODEL"; then
  ok "Model '$MODEL' already pulled"
else
  info "Pulling model '$MODEL' (one-time download, several GB)…"
  ollama pull "$MODEL"
  ok "Model '$MODEL' ready"
fi

# ---- 5. launch -------------------------------------------------------------
cat <<BANNER

${ORANGE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RST}
${ORANGE} HERA Copilot demo is ready${RST}

   👉 Open this one link — it logs you in and drops you straight
      into the tool (no account, no form):

       ${GREEN}${URL}/api/auth/demo-login${RST}

   Model: ${MODEL}  (running locally via Ollama)

   ${DIM}Want your own account? Open ${URL} and click "Create an${RST}
   ${DIM}account" — registration is open (just email + password).${RST}

   Press Ctrl-C to stop the demo.
${ORANGE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RST}

BANNER

# Single-port production mode: FastAPI serves the built SPA at $URL.
# debug=false disables the autoreloader (cleaner for a demo).
export HERA_DEBUG=false
export HERA_HOST="$HOST"
export HERA_PORT="$PORT"
export HERA_OLLAMA_MODEL="$MODEL"
export HERA_DEMO_MODE=true   # enables the /api/auth/demo-login magic link

exec uv run hera-web
