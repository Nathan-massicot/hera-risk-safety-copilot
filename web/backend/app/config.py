"""Runtime configuration for the HERA Copilot web app."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]
WEB_ROOT = REPO_ROOT / "web"
BACKEND_ROOT = WEB_ROOT / "backend"
FRONTEND_DIST = WEB_ROOT / "frontend" / "dist"
TAXONOMY_PATH = REPO_ROOT / "data" / "taxonomy" / "hera_taxonomy.json"
HERA_SVG_PATH = REPO_ROOT / "document" / "HERA_Taxonomy.svg"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="HERA_", extra="ignore")

    # App
    app_name: str = "HERA Copilot"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000

    # Storage
    db_path: Path = BACKEND_ROOT / "data" / "hera.db"
    transcripts_dir: Path = REPO_ROOT / "runs" / "web_transcripts"

    # Auth / sessions
    session_cookie_name: str = "hera_session"
    session_lifetime_hours: int = 12
    remember_me_lifetime_days: int = 30
    bcrypt_rounds: int = 12

    # Rate limiting (login attempts)
    login_max_attempts: int = 5
    login_window_minutes: int = 15

    # Ollama
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "mistral:7b-instruct-v0.3-q4_K_M"
    ollama_timeout_seconds: int = 120

    # CORS (only relevant when frontend dev server is on a different port)
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


settings = Settings()
settings.db_path.parent.mkdir(parents=True, exist_ok=True)
settings.transcripts_dir.mkdir(parents=True, exist_ok=True)
