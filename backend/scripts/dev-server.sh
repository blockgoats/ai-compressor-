#!/usr/bin/env bash
# Run FastAPI with reload (expects .venv + DB from dev-setup.sh).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT"

if [[ ! -d .venv ]]; then
  echo "Run ./scripts/dev-setup.sh first."
  exit 1
fi

PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
echo "API http://127.0.0.1:${PORT}/api/v1/health  (PORT=${PORT}, HOST=${HOST})"
# Use `python -m uvicorn` so we do not rely on the `uvicorn` console script shebang
# (it breaks if the venv was moved/renamed, e.g. ram/ → backend/).
exec .venv/bin/python -m uvicorn app.main:app --reload --host "$HOST" --port "$PORT"
