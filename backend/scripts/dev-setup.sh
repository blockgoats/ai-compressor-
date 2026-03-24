#!/usr/bin/env bash
# One-time / repeat: venv, install SDK + API deps, .env, optional Docker Postgres+Redis, init DB.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONPATH="$ROOT"

WITH_DOCKER="${WITH_DOCKER:-1}"

if [[ "$WITH_DOCKER" == "1" ]] && command -v docker &>/dev/null; then
  echo "==> Starting Postgres + Redis (docker compose)..."
  docker compose up -d postgres redis
  echo "==> Waiting for Postgres to accept connections..."
  sleep 5
  for _ in {1..25}; do
    if docker compose exec -T postgres pg_isready -U ram -d ramanujan &>/dev/null; then
      break
    fi
    sleep 1
  done
fi

if [[ ! -d .venv ]]; then
  echo "==> Creating virtualenv .venv"
  python3 -m venv .venv
fi

echo "==> pip install -e . && requirements-api.txt"
.venv/bin/pip install -U pip wheel -q
.venv/bin/pip install -e . -q
.venv/bin/pip install -r requirements-api.txt -q

if [[ ! -f .env ]]; then
  echo "==> Copy .env.example -> .env"
  cp .env.example .env
fi

echo "==> scripts/init_db.py"
PYTHONPATH="$ROOT" .venv/bin/python scripts/init_db.py

echo ""
echo "Done. Run the API:"
echo "  ./scripts/dev-server.sh"
echo "Or: make run"
