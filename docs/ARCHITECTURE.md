# Architecture

This repository is a **monorepo**: a Python **backend** (SDK + HTTP API) and a **React frontend**, plus **research docs** at the root.

```
┌─────────────┐     HTTP /api (dev proxy)     ┌──────────────────────────────────────┐
│  frontend/  │ ────────────────────────────► │  backend/                             │
│  (Vite SPA) │                               │  FastAPI app package: backend/app/  │
└─────────────┘                               │  (import name: app)                  │
                                              │  ramanujan_* packages + DB/Redis    │
                                              └──────────────────────────────────────┘
```

## Backend (`backend/`)

| Path | Role |
|------|------|
| `backend/app/` | FastAPI application (`app.main:app`), routes under `/api/v1` |
| `backend/ramanujan_compression/` | Core compression strategies (hybrid, sparse-modular, Fourier-like) |
| `backend/ramanujan_tokenizer/` | HuggingFace-style tokenizer integration |
| `backend/ramanujan_cli/` | Optional CLI |
| `backend/ramanujan_pro/` | Pro-tier extensions (optional deps) |

**Run locally:** from `backend/`, `make setup` then `make run` — see [`backend/BACKEND.md`](../backend/BACKEND.md).

The production compression path is **text → HF tokenizer → token IDs → `RamanujanCompressor` → decode** (string-level), not the full embedding-level RCP in [`whitepaper.md`](whitepaper.md). See [`WHITEPAPER_IMPLEMENTATION_NOTES.md`](WHITEPAPER_IMPLEMENTATION_NOTES.md).

## Frontend (`frontend/`)

Vite + React + TypeScript. In development, `npm run dev` serves the UI and **proxies** `/api` to `VITE_PROXY_TARGET` (default `http://127.0.0.1:8000`), so the browser can call the API same-origin. See [`frontend/.env.example`](../frontend/.env.example).

## Documentation (`docs/`)

| File | Purpose |
|------|---------|
| [`whitepaper.md`](whitepaper.md) | RCP paper (LaTeX source) |
| [`WHITEPAPER_IMPLEMENTATION_NOTES.md`](WHITEPAPER_IMPLEMENTATION_NOTES.md) | Paper vs shipped product |
| [`roadmap.md`](roadmap.md) | Full embedding RCP roadmap (funding-contingent) |

## Python package name vs folder name

- **Directory:** `backend/app/` — the FastAPI package.
- **Import:** `from app...` when `PYTHONPATH` is the `backend/` root (as in `make run` and Docker).

Do not confuse with the **`frontend/`** folder (the web app).
