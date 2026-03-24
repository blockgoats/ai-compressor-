# Contributing

Thank you for contributing to Ramj.

**New here?** Start with **[docs/ONBOARDING.md](docs/ONBOARDING.md)** (environment setup, running backend + frontend, first PR).

## Development setup

1. Fork the repository and clone your fork.
2. Create a branch: `git checkout -b short-description`.
3. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how `backend/`, `frontend/`, and `docs/` relate.
4. Follow the [root README](README.md) for `backend/` and/or `frontend/`.
5. Keep each pull request focused on a single concern.

## Checks before opening a PR

- **Frontend:** `cd frontend && npm run lint && npm run build`
- **Backend (syntax):** `python -m compileall -q backend/app` from the repo root
- **Backend (tests):** `cd backend && .venv/bin/python run_tests.py` (default runs pytest on `tests/`; use `--all` for imports + tests + examples), with venv and deps per [backend/BACKEND.md](backend/BACKEND.md)

## Pull requests

Describe what changed and why. Link related issues when applicable.

## Code style

- **Python:** Match existing modules (typing, FastAPI patterns).
- **TypeScript/React:** Match existing components; run `npm run lint` in `frontend/`.

## Research scope

- Paper source and roadmap live under [`docs/`](docs/README.md).
- Large **embedding-level RCP** changes should align with [`docs/roadmap.md`](docs/roadmap.md); open an issue first for very large work.

## License

By contributing, you agree your contributions are licensed under the [MIT License](LICENSE).
