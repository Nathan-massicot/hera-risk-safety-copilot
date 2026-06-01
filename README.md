# HERA Risk & Safety Copilot

A conversational AI copilot that helps mHealth app developers identify ethical and regulatory risks using the HERA taxonomy.

## Two ways to run it

| Interface | Path | Use it for |
|-----------|------|-----------|
| Gradio prototype (single-page) | `src/baseline/copilot.py` — `uv run hera-copilot` | Quick demos, model experimentation. |
| 3-page web app (FastAPI + React) | `web/` — `uv run hera-web` | Authenticated multi-user setup with onboarding, regulation diagram, and chatbot pages. See [`web/README.md`](web/README.md). |

Both share the HERA system-prompt builder and talk to a local Ollama server.

## Project documentation

- [`CLAUDE.md`](CLAUDE.md) — project spec, taxonomy, fine-tuning plan
- [`PROJECT_STATUS.md`](PROJECT_STATUS.md) — current state, gaps, and roadmap
- [`web/README.md`](web/README.md) — web app setup
- [`web/TODO.md`](web/TODO.md) — deferred items for the web app
