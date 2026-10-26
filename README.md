# RAG-as-a-Service (Project 1)

Production-shaped **Retrieval-Augmented Generation** backend — FastAPI + Postgres/**pgvector**.
Ingest documents, search them by meaning, and stream grounded, cited answers.

> Part of the [Applied AI Backend](docs/6-month-applied-ai-plan.md) learning path. Planning docs live in [docs/](docs/).

## What it does
- `POST /documents` — chunk → embed → store a document in pgvector
- `GET /documents`, `GET /documents/{id}` — list / fetch
- `POST /search` — semantic similarity search (top-k chunks + scores)
- `POST /chat` — streaming RAG answer (SSE) with inline citations
- `GET /health` — unauthenticated health check
- JWT auth on everything except `/health`

## Architecture

```
            ┌──────────── FastAPI (api/routes) ────────────┐
 client ──▶ │  /documents   /search   /chat   /health      │
            └───────┬───────────┬──────────┬───────────────┘
                    │           │          │
              ingestion    retrieval    rag.pipeline
                    │           │          │
              chunking     embeddings ◀────┘   llm (stream)
                    │           │
                    ▼           ▼
              ┌─────────────────────────┐      ┌─────────────┐
              │ Postgres + pgvector     │      │ LLM/Embed   │
              │ documents · chunks(vec) │      │ provider API│
              └─────────────────────────┘      └─────────────┘
```

## Layout
```
src/rag_service/
  main.py            # app entrypoint (uvicorn rag_service.main:app)
  config.py          # env-driven settings (pydantic-settings)
  api/
    deps.py          # auth dependency
    routes/          # documents, search, chat, health
  core/              # security (JWT), logging
  db/                # session, models (documents, chunks)
  schemas/           # request/response contracts (pydantic)
  services/          # chunking, embeddings, ingestion, retrieval, llm
  rag/pipeline.py    # retrieve → assemble context → generate
scripts/             # init_db.py, ingest_sample.py
tests/               # unit + integration
docs/                # the learning plan + notes
```

## Quickstart (local)
```bash
# 1. Python env + deps
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 2. Config
cp .env.example .env      # add your OPENAI_API_KEY

# 3. Database (pgvector) via Docker
make db                   # starts Postgres on :5432
make init                 # CREATE EXTENSION vector + tables

# 4. Run
make dev                  # http://localhost:8000/docs
```

Or the whole stack in Docker: `make up`.

## Try it
```bash
make ingest               # load the sample doc
# get a token (dev helper): python -c "from rag_service.core.security import create_access_token as t; print(t('dev'))"
# then POST /search or /chat with  Authorization: Bearer <token>
```

## Tech
FastAPI · SQLAlchemy 2 (async) · asyncpg · pgvector · Pydantic v2 · structlog · tenacity ·
OpenAI/Anthropic SDKs. Provider is swappable in `config.py`.

## Roadmap (maps to the plan)
- **Week 3:** ingestion + retrieval endpoints ✔ (scaffolded)
- **Week 4:** streaming chat + citations ✔, rate limiting, retries/timeouts, deploy to EC2
- **Month 3:** evals (RAGAS) + observability (Langfuse / custom)
- **Month 5:** hybrid search + re-ranking + better chunking
