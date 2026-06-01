# Regulatory documents corpus

Versioned set of regulatory PDFs used for:
- **Task #7 (RAG)** — ingested into ChromaDB, retrieved at inference time.
- **Task #12 (Cartographie)** — sources for the decision-tree content panels.

## Files

- `manifest.json` — single source of truth: id, title, publisher, URL, key articles, license, SHA256, access date.
- `*.pdf` — gitignored (large, copyright varies); not committed.

## How to populate

### Option A — Automatic (works for some sources)

```bash
uv run --extra dev python scripts/download_regulatory_docs.py
```

Hits each manifest URL with a polite User-Agent. Saves files matching
`filename` in the manifest. Updates `sha256` + `accessed` per entry.

Some publishers (e.g., European Commission CDN) return 403 to scripted
requests — that's expected. Fall back to Option B for those.

### Option B — Manual download (always works)

For any failed entry, open the URL in a browser, download the PDF, and save it
in `data/regulatory_docs/` with **exactly the filename from `manifest.json`**.

Then re-run the script — it will detect the existing file, compute the SHA256,
and update the manifest:

```bash
uv run --extra dev python scripts/download_regulatory_docs.py
```

### Option C — Just one doc

```bash
uv run --extra dev python scripts/download_regulatory_docs.py --only mdr_2017_745
```

## Priority for J2

Minimum viable set to start RAG (Task #7 on J3):

| Priority | Doc id | Manual download likely? |
|---|---|---|
| 1 | `eu_ai_act` | EU OJ direct PDF, usually OK auto |
| 1 | `mdr_2017_745` | EU OJ, usually OK auto |
| 1 | `gdpr_2016_679` | EU OJ, usually OK auto |
| 2 | `mdcg_2019_11` | Probably manual (403) |
| 2 | `who_lmm_health` | Manual (IRIS landing page) |
| 2 | `swiss_meddo` | Fedlex usually OK auto |
| 2 | `swiss_nldp` | Fedlex usually OK auto |
| 3 | `nice_esf`, `dtac` | Manual (NICE/NHS landing pages) |

If you're short on time, **doc ids 1 + 2 are enough for a defensible RAG**.

## Copyright / redistribution

- EU OJ regulations: public domain, free use.
- Swiss federal law (fedlex): public domain.
- MDCG guidance: free use with attribution (European Commission).
- WHO documents: CC BY-NC-SA 3.0 IGO.
- NICE / NHS: free for non-commercial.
- ISO standards: **paywalled** — `filename: null` in manifest. Cite, don't store.
- Beauchamp & Childress: **book, copyrighted** — cite only.

**All PDFs are gitignored.** They live on your machine only. The article cites
them via the manifest URLs + access dates + SHA256 hashes for reproducibility.

## Updating the manifest

After downloading any new doc, re-run the script — it recomputes the hash and
the `accessed` timestamp. Commit only `manifest.json`, never the PDFs.
