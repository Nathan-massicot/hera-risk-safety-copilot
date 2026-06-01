"""Download every regulatory PDF in the manifest, verify SHA256, and update the manifest.

Reads:  data/regulatory_docs/manifest.json
Writes: data/regulatory_docs/<filename> + an updated manifest with `sha256` + `accessed`

Skips:
- Entries with `filename: null` (paywalled or copyrighted — manual handling)
- URLs that don't return application/pdf (some are landing pages; manual download required)

Usage:
    uv run --extra dev python scripts/download_regulatory_docs.py
    uv run --extra dev python scripts/download_regulatory_docs.py --only mdr_2017_745
    uv run --extra dev python scripts/download_regulatory_docs.py --force
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.utils.logging_config import configure_logging, new_run_dir  # noqa: E402

log = logging.getLogger("docs")

DOCS_DIR = REPO_ROOT / "data/regulatory_docs"
MANIFEST = DOCS_DIR / "manifest.json"

USER_AGENT = "HERA-Copilot-Thesis-Project/0.1 (academic research; contact nathan2massicot@gmail.com)"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, dest: Path, force: bool) -> tuple[bool, str]:
    """Returns (downloaded, reason)."""
    if dest.exists() and not force:
        return False, f"already exists ({dest.stat().st_size:,} bytes)"
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=60, stream=True)
        r.raise_for_status()
    except requests.RequestException as exc:
        return False, f"HTTP error: {exc}"

    ctype = r.headers.get("Content-Type", "").lower()
    if "pdf" not in ctype and "octet-stream" not in ctype:
        return False, (
            f"Content-Type is '{ctype}', not a PDF — likely a landing page. "
            "Download manually."
        )

    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as fh:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                fh.write(chunk)
    return True, f"saved {dest.stat().st_size:,} bytes"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", help="Only fetch these document ids (can repeat)")
    ap.add_argument("--force", action="store_true", help="Re-download even if file exists")
    args = ap.parse_args(argv)

    run_dir = new_run_dir(prefix="docs")
    configure_logging(run_dir)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    documents = manifest["documents"]

    selected = (
        [d for d in documents if d["id"] in args.only]
        if args.only
        else documents
    )

    summary: list[dict] = []
    for doc in selected:
        did = doc["id"]
        fname = doc.get("filename")
        if not fname:
            log.info("⏭  %-25s  no filename (paywalled / book / manual) — skipping", did)
            summary.append({"id": did, "status": "skipped-no-filename"})
            continue

        url = doc["url"]
        dest = DOCS_DIR / fname
        log.info("→  %-25s  %s", did, url)
        downloaded, reason = fetch(url, dest, args.force)
        if not downloaded and "already exists" not in reason:
            log.warning("   %s", reason)
            summary.append({"id": did, "status": "failed", "reason": reason})
            continue
        log.info("   %s", reason)

        if dest.exists():
            doc["sha256"] = sha256_of(dest)
            doc["bytes"] = dest.stat().st_size
            doc["accessed"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            summary.append({"id": did, "status": "ok", "sha256": doc["sha256"][:12]})

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log.info("Manifest updated: %s", MANIFEST.relative_to(REPO_ROOT))

    # Summary
    log.info("\nSummary:")
    for s in summary:
        log.info("  %s  %s", s["status"], s["id"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
