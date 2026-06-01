# HERA Copilot — Web app

3-page web interface around the HERA Risk & Safety Copilot:

1. **Onboarding** — interactive form that captures app metadata + research consent.
2. **Regulation diagram** — placeholder showing the HERA taxonomy SVG (interactive version on the TODO list).
3. **Chatbot** — chat UI talking to a local Ollama model, with the HERA system prompt pre-loaded with the user's onboarding context.

Login is invite-only (admin generates tokens via CLI), passwords are hashed with bcrypt, and sessions are stored server-side with HTTP-only cookies (with optional 30-day "remember me").

## Layout

```
web/
├── backend/             FastAPI + SQLAlchemy + SQLite
│   ├── app/
│   │   ├── main.py      Entry point (uv run hera-web)
│   │   ├── config.py    Settings (env-driven)
│   │   ├── db.py        SQLite engine + session
│   │   ├── models.py    User, Session, InviteToken, OnboardingProfile, Conversation, Message
│   │   ├── security.py  bcrypt, session tokens, login rate-limit
│   │   ├── ollama_client.py  Reuses the HERA system-prompt builder from src/baseline/copilot.py
│   │   └── routers/     auth · onboarding · chat
│   └── cli.py           uv run hera-cli (invite create / list, user reset-password)
├── frontend/            Vite + React + TypeScript + Tailwind (grey/white + #FF6B1A)
└── TODO.md              Deferred items (HTTPS deploy, streaming, logo, multi-conversation…)
```

## First-time setup

### 1. Install backend deps

```bash
uv sync --extra web
```

### 2. Install frontend deps

```bash
cd web/frontend
npm install
```

### 3. Make sure Ollama is running

```bash
ollama serve                                        # in one terminal
ollama pull mistral:7b-instruct-v0.3-q4_K_M         # only first time
```

### 4. Create yourself an invite token

```bash
uv run hera-cli invite create --note "Nathan"
# → Invite token: <copy this>
```

## Run (development)

In two terminals:

```bash
# 1) backend (http://127.0.0.1:8000)
uv run hera-web

# 2) frontend (http://127.0.0.1:5173) — proxies /api → backend
cd web/frontend && npm run dev
```

Open http://127.0.0.1:5173, click **Create an account**, paste the invite token, fill in the onboarding form (consent checkbox required), and you land on the chatbot.

## Run (production-style — single port)

Build the frontend, then start the backend; FastAPI serves the built SPA at the same origin.

```bash
cd web/frontend && npm run build
cd ../..
uv run hera-web
# → open http://127.0.0.1:8000
```

## Configuration

All settings can be overridden via env vars prefixed with `HERA_`. Notable ones:

| Variable | Default | Purpose |
|----------|---------|---------|
| `HERA_OLLAMA_URL` | `http://localhost:11434` | Ollama HTTP base URL |
| `HERA_OLLAMA_MODEL` | `mistral:7b-instruct-v0.3-q4_K_M` | Chatbot model |
| `HERA_HOST` | `127.0.0.1` | Backend bind address |
| `HERA_PORT` | `8000` | Backend port |
| `HERA_SESSION_LIFETIME_HOURS` | `12` | Default session length |
| `HERA_REMEMBER_ME_LIFETIME_DAYS` | `30` | "Remember me" length |
| `HERA_LOGIN_MAX_ATTEMPTS` | `5` | Failed logins per window before 429 |
| `HERA_LOGIN_WINDOW_MINUTES` | `15` | Rate-limit window |

## Data

- SQLite DB → `web/backend/data/hera.db`
- Per-user JSONL transcripts → `runs/web_transcripts/<email>/conversation_<id>.jsonl`

Both directories are git-ignored.

## See also

- [`TODO.md`](TODO.md) — deferred items
- [`../CLAUDE.md`](../CLAUDE.md) — project spec
- [`../PROJECT_STATUS.md`](../PROJECT_STATUS.md) — research roadmap
