# Ramj

**Ramanujan-inspired prompt compression** — Python SDK, FastAPI service, and React dashboard for token-efficient LLM prompts.

<!-- After publishing: replace YOUR_ORG and YOUR_REPO in the CI badge URL -->
[![CI](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/YOUR_ORG/YOUR_REPO/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CODE_OF_CONDUCT.md)

| | |
|--|--|
| **License** | [MIT](LICENSE) |
| **Stack** | `backend/` FastAPI + SDK · `frontend/` Vite + React + TypeScript |

> **Scope:** Production uses **tokenizer + `ramanujan_compression`** on text prompts. Full **embedding-level RCP** and **soft prompts** from the paper are documented as a [funding-contingent roadmap](docs/roadmap.md); see [implementation notes](docs/WHITEPAPER_IMPLEMENTATION_NOTES.md).

## Repository layout

```
backend/      SDK (ramanujan_compression, tokenizer, CLI) + FastAPI app in backend/app/
frontend/     Dashboard SPA (Vite); proxies /api to the backend in dev
docs/         Whitepaper (LaTeX), roadmap, architecture, paper vs product notes
```

See **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** for a diagram and naming notes (`app` = Python package, `frontend/` = web UI).

## Quick start

### Backend (API & SDK)

```bash
cd backend
cp .env.example .env   # SECRET_KEY, DATABASE_URL, Redis; optional OPENAI_API_KEY / GROQ_API_KEY
make setup             # venv, pip install -e ., requirements-api.txt, optional Docker Postgres/Redis
make deps              # Postgres + Redis only (Docker)
make run               # http://127.0.0.1:8000 — OpenAPI at /docs
```

- **Details:** [backend/BACKEND.md](backend/BACKEND.md) (routes, Docker, **venv troubleshooting** if the project folder was moved or renamed).
- **SDK overview:** [backend/PROJECT_SUMMARY.md](backend/PROJECT_SUMMARY.md).

### Frontend

```bash
cd frontend
cp .env.example .env.local   # optional: VITE_API_BASE_URL, VITE_PROXY_TARGET (default API http://127.0.0.1:8000)
npm install
npm run dev
```

Production build: `npm run build` → `frontend/dist/` (gitignored). The dev server proxies **`/api`** to the backend so the UI can use relative `/api/...` URLs.

### Full stack (local)

1. Start **backend:** `cd backend && make run` (port **8000** by default).
2. Start **frontend:** `cd frontend && npm run dev` (Vite default port **5173**; ensure `VITE_PROXY_TARGET` matches the API).

## Configuration

| Area | File |
|------|------|
| Backend | [backend/.env.example](backend/.env.example) |
| Frontend | [frontend/.env.example](frontend/.env.example) |

Do not commit real `.env` files. Use a strong `SECRET_KEY` and real DB credentials in production.

## Documentation index

| | |
|--|--|
| **Contributor onboarding** | [docs/ONBOARDING.md](docs/ONBOARDING.md) |
| **Index** | [docs/README.md](docs/README.md) |
| **Architecture** | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| **Contributing** | [CONTRIBUTING.md](CONTRIBUTING.md) |
| **Code of Conduct** | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| **Changelog** | [CHANGELOG.md](CHANGELOG.md) |
| **Security** | [SECURITY.md](SECURITY.md) |

## Publishing this repository

1. Review the tree for secrets and internal-only material before going public.
2. Push to GitHub (example):

```bash
git remote add origin https://github.com/YOUR_ORG/YOUR_REPO.git
git push -u origin main
```

3. Enable **private vulnerability reporting** (GitHub → **Security**) if you use [SECURITY.md](SECURITY.md).

## License

[MIT License](LICENSE). Third-party dependencies remain under their own licenses.
