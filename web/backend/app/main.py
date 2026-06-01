"""FastAPI entry point — wires routers, static files, and CORS."""

from __future__ import annotations

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from .config import FRONTEND_DIST, HERA_SVG_PATH, settings
from .db import init_db
from .routers import auth, chat, onboarding


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(onboarding.router)
app.include_router(chat.router)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/diagram/hera.svg")
def hera_diagram() -> Response:
    if not HERA_SVG_PATH.exists():
        return Response(status_code=404)
    return FileResponse(HERA_SVG_PATH, media_type="image/svg+xml")


# --- Static frontend (only when the React app has been built) ---------------

if FRONTEND_DIST.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIST / "assets"),
        name="assets",
    )

    @app.get("/{full_path:path}")
    def spa_fallback(full_path: str):
        # Any unmatched GET serves the SPA's index.html so React Router can
        # handle client-side routing.
        if full_path.startswith("api/"):
            return Response(status_code=404)
        index = FRONTEND_DIST / "index.html"
        if index.exists():
            return FileResponse(index, media_type="text/html")
        return Response(status_code=404)


def run() -> None:
    """Console-script entry point (`uv run hera-web`)."""
    uvicorn.run(
        "web.backend.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    run()
