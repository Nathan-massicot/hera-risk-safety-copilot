# HERA Risk & Safety Copilot

A conversational AI copilot that helps mHealth app developers identify ethical
and regulatory risks using the **HERA taxonomy** (7 pillars, 37 dimensions).
The chatbot is **retrieval-augmented** over a curated corpus of regulatory
cards (GDPR, EU AI Act, MDR, Swiss nFADP/MedDO, …) and runs entirely on a
**local model** — no API keys, no data leaving your machine.

## Quick demo (one command)

After cloning, just run:

```bash
./demo.sh
```

It installs dependencies, ensures a local Ollama model is available, rebuilds
the RAG index from the committed regulatory cards, and serves the whole app on
a single URL. When it finishes it prints a **one-click magic link** — open it
and you land straight in the chatbot (no account, no token, no onboarding form):

```
http://127.0.0.1:8000/api/auth/demo-login
```

You arrive as a pre-onboarded demo app ("CardioCompanion", a hypertension
self-management app deployed in the EU + Switzerland), so the copilot already
has context to reason over GDPR / MDR / EU AI Act / nFADP.

> Prefer the real flow? The script also prints an invite token — open
> http://127.0.0.1:8000, click **Create an account**, and paste it.

### Prerequisites

The script checks for these and tries to auto-install them where it can
([Homebrew](https://brew.sh) on macOS, the official installer on Linux):

- [`uv`](https://docs.astral.sh/uv/) — Python dependency manager
- **Node.js 18+** — to build the React frontend
- [**Ollama**](https://ollama.com/download) — runs the local LLM

**First run is heavy and slow**: it downloads the chat model (`qwen3:8b`,
several GB), the embedding model, and ~1–2 GB of Python deps (`torch`,
`sentence-transformers`). Every run afterwards is fast.

```bash
HERA_OLLAMA_MODEL=qwen3:4b ./demo.sh   # smaller/faster chat model download
```

## What's inside

The web app (FastAPI + React, single origin) has three pages behind an
invite-only login:

| Page | What it does |
|------|--------------|
| **HERA Chatbot** | RAG-augmented chat that interviews you about your app, flags risks against HERA dimensions with regulatory citations, and can synthesize a structured risk report. |
| **Regulation diagram** | Interactive HERA taxonomy — pillars, dimensions, and their mapped regulatory sources. |
| **Decision tree** | Guided jurisdiction/classification walkthrough (EU vs. Switzerland, SaMD, etc.). |

## Two ways to run it

| Interface | Path | Use it for |
|-----------|------|-----------|
| Gradio prototype (single-page) | `src/baseline/copilot.py` — `uv run hera-copilot` | Quick demos, model experimentation. |
| 3-page web app (FastAPI + React) | `web/` — `uv run hera-web` | The full authenticated app. See [`web/README.md`](web/README.md) for manual/dev setup (two-terminal dev mode, config, etc.). |

Both share the HERA system-prompt builder and talk to a local Ollama server.

## Architecture, briefly

```
Browser ── http://127.0.0.1:8000 ──► FastAPI (serves the built React SPA + /api)
                                          │
                       ┌──────────────────┼───────────────────┐
                       ▼                  ▼                   ▼
                 SQLite (auth,      Chroma index over     Ollama (local LLM,
                 sessions, chats)   regulatory cards      qwen3:8b) — generation
                                    (RAG retrieval)
```

`demo.sh` runs everything in single-port production mode (FastAPI serves the
built SPA), so there's one URL and one process to reason about.

## Project documentation

- [`docclaude/CLAUDE.md`](docclaude/CLAUDE.md) — project spec, taxonomy, fine-tuning plan
- [`docclaude/PROJECT_STATUS.md`](docclaude/PROJECT_STATUS.md) — current state, gaps, and roadmap
- [`web/README.md`](web/README.md) — web app setup (manual / dev)
- [`web/TODO.md`](web/TODO.md) — deferred items for the web app
