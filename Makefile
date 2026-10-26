.PHONY: install dev db init ingest test lint fmt up down

install:       ## Install app + dev deps into the active venv
	pip install -e ".[dev]"

dev:           ## Run the API with autoreload
	uvicorn rag_service.main:app --reload

db:            ## Start only Postgres (pgvector) via compose
	docker compose up -d db

init:          ## Enable pgvector + create tables
	python scripts/init_db.py

ingest:        ## Ingest the sample document
	python scripts/ingest_sample.py data/samples/sample.txt

test:          ## Run tests
	pytest -q

lint:          ## Lint + type-check
	ruff check src tests && mypy src

fmt:           ## Auto-format / fix imports
	ruff check --fix src tests

up:            ## Build + run the whole stack (app + db)
	docker compose up --build

down:          ## Stop the stack
	docker compose down
