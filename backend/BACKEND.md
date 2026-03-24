# Ramanujan Compression — FastAPI backend

This tree is the **Ramanujan Compression SDK** (`ramanujan_compression`, `ramanujan_tokenizer`, …) plus a **production-style HTTP API** in the Python package **`app/`** (path: `backend/app/`).

## Stack

- FastAPI (async), Pydantic v2, Uvicorn  
- PostgreSQL + SQLAlchemy 2 async (`asyncpg`)  
- Redis (rate limiting / cache hooks; Celery broker)  
- Celery worker (`app/workers/celery_app.py`)  

## Quick start (local)

**Automated (recommended):**

```bash
cd /path/to/backend
chmod +x scripts/dev-setup.sh scripts/dev-server.sh
./scripts/dev-setup.sh    # venv, pip, .env, docker postgres+redis, init_db
./scripts/dev-server.sh   # API on http://0.0.0.0:8000
```

Or: `make setup` then `make run`.

Skip Docker deps (use your own Postgres): `WITH_DOCKER=0 ./scripts/dev-setup.sh`

**Manual:**

```bash
cd /path/to/backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
pip install -r requirements-api.txt
cp .env.example .env
# Start Postgres + Redis (e.g. docker compose up -d postgres redis)
export PYTHONPATH=.
python scripts/init_db.py
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Prefer `python -m uvicorn` over the `uvicorn` script so the interpreter path stays correct if the project directory is moved.

Open `http://127.0.0.1:8000/api/v1/health` and `http://127.0.0.1:8000/docs`.

With `AUTH_DISABLE=true`, JWT is optional on compress/generate routes.

### Troubleshooting: `uvicorn: cannot execute` or `required file not found`

The virtualenv was probably created under an old path (for example before renaming `ram/` to `backend/`). Console scripts like `uvicorn` embed that path in their shebang. **`make run` uses `python -m uvicorn`** to avoid that; if errors persist, recreate the venv:

```bash
cd backend
rm -rf .venv
./scripts/dev-setup.sh   # or: python3 -m venv .venv && .venv/bin/pip install -e . -r requirements-api.txt
```

## Docker (API + Postgres + Redis + Celery)

```bash
docker compose up --build
```

API: `http://localhost:8000/api/v1/`.

## Main routes (`/api/v1`)

| Method | Path | Notes |
|--------|------|--------|
| POST | `/compress` | Uses SDK `RamanujanCompressor` + HF tokenizer (see `backend/app/services/compression_service.py`) |
| POST | `/token-estimate` | Fast preview (estimate-only path) |
| POST | `/generate` | Compress → OpenAI-compatible chat (set `OPENAI_API_KEY` or `GROQ_API_KEY`) |
| GET | `/analytics/overview` | Aggregates `analytics_events` |
| GET | `/analytics/history` | Time series of token savings |
| POST | `/cost-simulate` | Monthly cost illustration |
| POST | `/replay-payload` | Reproducibility payload for `/compress` |
| GET | `/demo/prompts` | Sample prompts |
| POST | `/playground/sessions` | Store playground runs |
| POST | `/prompts/{id}/versions` | Prompt versioning |
| POST | `/auth/register`, `/auth/login` | JWT |
| GET | `/health` | Liveness |

## Compression integration

- **Lossless**: whitespace normalization; no token-ID compression.  
- **Lossy / ramanujan**: `ramanujan_compression.RamanujanCompressor` with mapped `CompressionStrategy` and levels (`low` / `medium` / `aggressive` → target ratios in `compression_service.py`).

## Next steps (production hardening)

- Alembic migrations instead of `scripts/init_db.py` only  
- Redis-backed rate limiting (e.g. SlowAPI + Redis)  
- API key table + `X-API-Key` middleware  
- Wire Celery for long-running compress jobs  
