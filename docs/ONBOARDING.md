# Onboarding for contributors

Welcome. This guide gets you from **zero to a running dev environment** and your **first PR** without duplicating every detail elsewhere—use it as a checklist.

| If you need… | Read |
|--------------|------|
| How folders connect | [ARCHITECTURE.md](ARCHITECTURE.md) |
| API env, Docker, routes, troubleshooting | [backend/BACKEND.md](../backend/BACKEND.md) |
| SDK modules, CLI, tests | [backend/PROJECT_SUMMARY.md](../backend/PROJECT_SUMMARY.md) |
| Paper vs shipped product | [WHITEPAPER_IMPLEMENTATION_NOTES.md](WHITEPAPER_IMPLEMENTATION_NOTES.md) |
| PR rules and checks | [CONTRIBUTING.md](../CONTRIBUTING.md) |

---

## 1. Prerequisites

Install these on your machine (versions are indicative; match CI when possible):

| Tool | Typical version | Used for |
|------|-----------------|----------|
| **Git** | recent | clone, branches, PRs |
| **Python** | 3.11+ (3.12 OK) | backend, venv — see [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| **Node.js** | 22 LTS (or CI version) | frontend (`npm`) |
| **Docker** | optional but recommended | Postgres + Redis for `make setup` in `backend/` |

You do **not** need a GPU for the default API + UI work.

---

## 2. Clone and fork workflow

1. **Fork** the repo on GitHub (if you lack push access).
2. Clone **your fork** (or the org repo if you are a maintainer):

   ```bash
   git clone https://github.com/YOUR_USERNAME/ramj.git
   cd ramj
   ```

3. Add upstream if you use a fork:

   ```bash
   git remote add upstream https://github.com/ORG/ramj.git   # adjust URL
   ```

4. Create a **feature branch** off `main`:

   ```bash
   git checkout main
   git pull upstream main   # or origin main
   git checkout -b feat/your-topic
   ```

Naming: `feat/…`, `fix/…`, or `docs/…` keeps history readable.

---

## 3. Backend setup (`backend/`)

The API and SDK live under **`backend/`**. The FastAPI Python package is named **`app`** and lives at **`backend/app/`** (imports look like `from app.api...` when `PYTHONPATH` is `backend/`).

### Quick path (recommended)

```bash
cd backend
cp .env.example .env
# Edit .env: SECRET_KEY, DATABASE_URL, Redis URLs if not using Docker defaults
make setup      # venv, pip install -e ., requirements-api.txt, optional Docker PG+Redis, init_db
make run        # API at http://127.0.0.1:8000 — OpenAPI at /docs
```

- **Health:** `GET http://127.0.0.1:8000/api/v1/health`
- **Interactive docs:** `http://127.0.0.1:8000/docs`

### If `make setup` fails

- Ensure Docker is running if you rely on `docker compose` for Postgres/Redis, or set `WITH_DOCKER=0` and point `.env` at your own databases (see [BACKEND.md](../backend/BACKEND.md)).
- If **`uvicorn: cannot execute`** or **`required file not found`**, the venv was likely created under an old path. From `backend/`:

  ```bash
  rm -rf .venv
  ./scripts/dev-setup.sh
  ```

  `make run` uses **`python -m uvicorn`** to avoid broken console-script shebangs.

### Backend tests (before a PR)

From repo root (with venv activated or using full paths):

```bash
cd backend
.venv/bin/python run_tests.py          # default: pytest on tests/
python -m compileall -q app            # quick syntax check from backend/
```

From repo root: `python -m compileall -q backend/app`.

---

## 4. Frontend setup (`frontend/`)

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

- Dev server defaults to **port 5173** (Vite).
- It **proxies** `/api` to **`VITE_PROXY_TARGET`** (default `http://127.0.0.1:8000`). Start the **backend first** on 8000, or change the target in `.env.local`.

### Frontend checks (before a PR)

```bash
cd frontend
npm run lint
npm run build
```

---

## 5. Full stack (typical day)

1. Terminal A: `cd backend && make run`
2. Terminal B: `cd frontend && npm run dev`
3. Open the URL Vite prints (e.g. `http://localhost:5173`). API calls use `/api/...` through the proxy.

---

## 6. Where to change code

| Goal | Likely location |
|------|----------------|
| HTTP routes, auth, compress/generate | `backend/app/api/` |
| Compression pipeline, tokenizer wiring | `backend/app/services/` |
| Core algorithms | `backend/ramanujan_compression/` |
| UI pages and components | `frontend/src/` |
| Env-driven API URL / proxy | `frontend/.env.local`, `frontend/vite.config.ts` |
| Paper / roadmap text only | `docs/` |

Avoid drive-by refactors outside your task; match existing style (see [CONTRIBUTING.md](../CONTRIBUTING.md)).

---

## 7. Opening a pull request

1. Push your branch to your fork: `git push -u origin feat/your-topic`
2. Open a PR against **`main`** (or the branch maintainers use).
3. In the description: **what** changed, **why**, and how you **tested** (e.g. “lint + build frontend”, “hit /compress locally”).
4. Run the **checks** in [CONTRIBUTING.md](../CONTRIBUTING.md) before requesting review.

---

## 8. Getting unstuck

| Symptom | Hint |
|---------|------|
| `ModuleNotFoundError: app` | Run API from `backend/` with `PYTHONPATH` set (use `make run` / `dev-server.sh`). |
| CORS or 404 on `/api` in browser | Use the Vite dev proxy; don’t call a different origin unless `VITE_API_BASE_URL` is set intentionally. |
| Database errors | Postgres/Redis up? `.env` URLs match Docker hostnames vs `localhost`? |
| “Paper says X but API does Y” | Expected—read [WHITEPAPER_IMPLEMENTATION_NOTES.md](WHITEPAPER_IMPLEMENTATION_NOTES.md). |

Open a **GitHub issue** for bugs or design questions; large **embedding-level RCP** work should align with [roadmap.md](roadmap.md) and usually needs discussion first.

---

## 9. Community standards

Participation is governed by the [Code of Conduct](../CODE_OF_CONDUCT.md). For maintainer process and releases, see [Governance](../GOVERNANCE.md) and [RELEASING.md](../RELEASING.md).

## 10. License

Contributions are under the [MIT License](../LICENSE) (see [CONTRIBUTING.md](../CONTRIBUTING.md)).
