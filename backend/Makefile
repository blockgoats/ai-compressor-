.PHONY: setup deps run docker-up docker-all help

help:
	@echo "make setup   - venv, pip install, .env, docker postgres+redis, init_db"
	@echo "make deps    - only docker compose postgres + redis"
	@echo "make run     - uvicorn app.main:app --reload on :8000"
	@echo "make docker-all - full stack (api + celery + postgres + redis)"

setup:
	@chmod +x scripts/dev-setup.sh scripts/dev-server.sh 2>/dev/null || true
	@./scripts/dev-setup.sh

deps:
	docker compose up -d postgres redis

run:
	@chmod +x scripts/dev-server.sh 2>/dev/null || true
	@./scripts/dev-server.sh

docker-all:
	docker compose up --build
