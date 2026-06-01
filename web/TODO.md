# Web app — deferred work

Items deferred during the initial scaffold (2026-04-28).

## Deployment & infrastructure
- [ ] Deploy beyond `localhost` (pick host: BFH server / Fly.io / Render).
- [ ] Enable HTTPS and flip the session cookie `secure=True` (in `web/backend/app/routers/auth.py`, `_set_session_cookie`).
- [ ] Stronger CSRF protection once cookies leave the local machine (currently relies on `SameSite=lax` + same-origin).
- [ ] Production CORS allow-list — remove `localhost:5173` once frontend is built and served by FastAPI.

## Chatbot UX
- [ ] Token-by-token streaming via `/api/chat/stream` (Server-Sent Events) — current `/api/chat/message` returns the full response in one shot.
- [ ] Render assistant Markdown (the existing risk reports include `##`, lists, **bold**) via `react-markdown`.
- [ ] Multi-conversation history sidebar (currently one active conversation per user).
- [ ] Re-introduce a "Generate risk report" button.

## Regulation diagram page
- [ ] Replace the static SVG embed with an interactive D3 / SVG explorer:
  click each pillar → drill into dimensions → click a dimension → show source
  framework citations + example risks + mitigations from `hera_taxonomy.json`.

## Branding
- [ ] Design a proper logo (placeholder is the letter "H" on a dark background).
- [ ] Pick a final favicon.

## Auth
- [ ] Self-serve password reset via email magic link.
- [ ] 2FA (TOTP) for admin accounts.
- [ ] Audit-log table (login, logout, profile edit, conversation reset).

## Quality
- [ ] Backend tests under `web/backend/tests/` (auth flow, onboarding, chat — Ollama mocked).
- [ ] Playwright smoke test for the 3-page flow.
- [ ] CI: lint + tests on push (extend existing GitHub Actions plan from `PROJECT_STATUS.md`).
