# Ramj frontend

React dashboard for **Ramanujan Compression** — React 19, TypeScript, Vite 8, Tailwind CSS 4.

## Prerequisites

A running API on the URL you proxy to (default **`http://127.0.0.1:8000`**). From the repo root, start the backend first:

```bash
cd ../backend && make run
```

See [backend/BACKEND.md](../backend/BACKEND.md) for environment variables and troubleshooting.

## Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Dev server; proxies **`/api`** to `VITE_PROXY_TARGET` |
| `npm run build` | Production build → `dist/` |
| `npm run lint` | ESLint |

## Configuration

Copy [`.env.example`](.env.example) to `.env.local`.

| Variable | Purpose |
|----------|---------|
| `VITE_PROXY_TARGET` | Backend origin for the dev proxy (default `http://127.0.0.1:8000`) |
| `VITE_API_BASE_URL` | Optional explicit API origin; leave empty to use same-origin `/api` via proxy |

Full stack overview: [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) · [root README](../README.md).
