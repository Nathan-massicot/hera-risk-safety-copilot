"""FastAPI entry point — wires routers, static files, and CORS."""

from __future__ import annotations

import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from .config import (
    DECISION_TREE_PATH,
    FRONTEND_DIST,
    HERA_SVG_PATH,
    TAXONOMY_PATH,
    settings,
)
from .db import init_db
from .routers import auth, chat


def _load_taxonomy() -> dict:
    """Base HERA taxonomy with each dimension enriched by its mapped regulatory
    citations (data/taxonomy/_dim_sources/<id>.json, produced by the enrichment
    workflow). Missing source files just yield an empty `sources` list."""
    taxonomy = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    sources_dir = TAXONOMY_PATH.parent / "_dim_sources"
    for pillar in taxonomy["pillars"]:
        for dim in pillar["dimensions"]:
            f = sources_dir / f"{dim['id']}.json"
            if f.exists():
                try:
                    dim["sources"] = json.loads(f.read_text(encoding="utf-8")).get("sources", [])
                except (json.JSONDecodeError, OSError):
                    dim["sources"] = []
            else:
                dim["sources"] = []
    return taxonomy


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
app.include_router(chat.router)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/diagram/hera.svg")
def hera_diagram() -> Response:
    if not HERA_SVG_PATH.exists():
        return Response(status_code=404)
    return FileResponse(HERA_SVG_PATH, media_type="image/svg+xml")


@app.get("/api/taxonomy")
def taxonomy() -> dict:
    if not TAXONOMY_PATH.exists():
        raise HTTPException(status_code=404, detail="Taxonomy file not found")
    return _load_taxonomy()


@app.get("/api/decision-tree")
def decision_tree() -> dict:
    if not DECISION_TREE_PATH.exists():
        raise HTTPException(status_code=404, detail="Decision tree file not found")
    return json.loads(DECISION_TREE_PATH.read_text(encoding="utf-8"))


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
