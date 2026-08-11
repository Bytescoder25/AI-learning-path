# Detailed 24-Week Execution Plan — Applied AI Backend Engineer

This is the step-by-step expansion of [6-month-applied-ai-plan.md](6-month-applied-ai-plan.md). Same scope, same 5 projects, same "no math / no training models" boundary — but broken down into 24 individual weeks with concrete daily-level actions, checklists, specific packages/commands, and exact deliverables so no small step gets missed.

**How to use this file:**
- Each week has: **Learn** (what to read/watch), **Build** (what to actually type/run), **Checklist** (tick before moving on), and **Definition of done** for that week.
- Follow the cadence from the original plan: 2×~1hr weekdays (learn + small experiment), 1×4-6hr weekend block (build), Sunday 15-min commit + public progress note.
- If a week's checklist isn't done, it's fine to spill into the weekend of the next week — but don't skip the checklist items, just slow down.
- **Applications start Week 21**, in parallel with the remaining build work — don't wait for Week 24.

---

## Month 1 (Weeks 1–4) — Foundations + Project 1: RAG-as-a-Service

### Week 1 — LLM fundamentals + prompt/context engineering

**Learn**
- [ ] Tokens & tokenization: run text through a tokenizer (e.g. OpenAI's `tiktoken` or the Anthropic token counting API) and see how words split into tokens. Understand why this affects cost and context limits.
- [ ] Context windows: know the context limit of the model(s) you'll use (e.g. Claude, GPT). Understand what happens when you exceed it (truncation/errors) and why "stuffing everything into the prompt" doesn't scale.
- [ ] Temperature & sampling params (top_p, max_tokens): run the same prompt at temperature 0 vs 1 and compare outputs.
- [ ] Embeddings: understand that an embedding is a vector representation of meaning; two similar texts → vectors close together (cosine similarity).
- [ ] Structured/JSON output: learn how to force a model to return valid JSON (response_format / tool-forced JSON / schema-constrained output).
- [ ] Function/tool calling basics: understand the request/response shape — model returns a "call this function with these args" instead of plain text.
- [ ] Streaming: understand server-sent events / chunked responses and why they matter for perceived latency.
- [ ] Cost & latency: read the pricing page for your chosen provider(s); calculate cost per 1K requests for a typical prompt+completion size.
- [ ] Read/skim: DeepLearning.AI short course "ChatGPT Prompt Engineering for Developers."

**Resources (free)**
- [ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/) — DeepLearning.AI, ~1.5hr, free to watch (labs/cert need Pro).
- **AI Prompting for Everyone** — DeepLearning.AI, ~7hr, free to watch, broader prompting fundamentals.

**Build (small daily experiments, not the full project yet)**
- [ ] Get API keys set up (Anthropic and/or OpenAI) in a `.env` file, never committed.
- [ ] Write a 20-line Node.js script that calls the model with a plain prompt and prints the response.
- [ ] Modify it to stream the response token-by-token to stdout.
- [ ] Modify it to force JSON output matching a small schema (e.g. `{name, age, tags[]}`).
- [ ] Write a script that defines one dummy "tool" (e.g. `getWeather(city)`) and confirms the model calls it correctly.

**Checklist**
- [ ] Can explain tokens, context window, temperature, embeddings, JSON mode, function calling, streaming in your own words (you'll need this for interviews later).
- [ ] Have working API access to at least one model provider.
- [ ] Have 3–4 small throwaway scripts proving each concept above.

---

### Week 2 — Prompt/context engineering deep dive + RAG architecture + pgvector setup

**Learn**
- [ ] System prompts vs user prompts vs few-shot examples — when each is the right lever.
- [ ] Context assembly: how a real app builds the final prompt (system instructions + retrieved docs + chat history + user query) and orders/truncates them.
- [ ] Prompt templates & versioning: why prompts should be treated like config, not hardcoded strings.
- [ ] RAG architecture end-to-end: chunking strategies (fixed-size, sentence-aware, recursive), embedding generation, vector search (ANN/cosine), retrieval, re-ranking, and citation/attribution back to source chunks.
- [ ] pgvector: read the extension docs — `CREATE EXTENSION vector;`, the `vector` column type, distance operators (`<->`, `<=>`), and index types (`ivfflat` vs `hnsw`).
- [ ] Read/skim: DeepLearning.AI "Building Systems with the ChatGPT API."

**Resources (free)**
- [Krish Naik — Introduction to Understanding RAG](https://www.classcentral.com/course/youtube-introduction-to-undertsanding-rag-retrieval-augmented-generation-480511) — free 21-min YouTube primer on RAG.
- "Complete RAG Tutorial 2026" — free YouTube walkthrough building a RAG app from scratch.
- [pgvector GitHub README](https://github.com/pgvector/pgvector) — official docs, no dedicated free video course exists for pgvector specifically.

**Build**
- [ ] Install PostgreSQL locally (or use your existing instance) + enable pgvector (`CREATE EXTENSION IF NOT EXISTS vector;`).
- [ ] Design the schema: `documents` table (id, source, metadata) + `chunks` table (id, document_id, content, embedding vector(1536), created_at).
- [ ] Write a script that: reads a sample text file → chunks it (start simple: fixed-size with overlap) → calls an embeddings API → inserts rows into `chunks`.
- [ ] Write a raw SQL query using `<=>` (cosine distance) to find the top-5 nearest chunks to a test embedding.
- [ ] Create an `hnsw` or `ivfflat` index on the embedding column and confirm the query plan uses it (`EXPLAIN ANALYZE`).

**Checklist**
- [ ] pgvector extension installed and working locally.
- [ ] Can chunk a document and store embeddings in Postgres.
- [ ] Can run a similarity search query and get sensible nearest neighbors back.
- [ ] Understand chunking trade-offs (too small = loses context, too big = dilutes relevance).

---

### Week 3 — Project 1 backend: ingestion + retrieval

**Build (Project 1 — RAG-as-a-Service backend)**
- [ ] Scaffold a new Node.js/Express project (or reuse a boilerplate): `npm init`, `express`, `dotenv`, `pg`, plus **Vercel AI SDK** (`ai` package) or **LangChain.js**.
- [ ] Set up project structure: `/src/routes`, `/src/services`, `/src/db`, `/src/middleware`.
- [ ] Implement `POST /documents` — accepts a document (text or file upload), chunks it, embeds each chunk, stores in Postgres via pgvector.
- [ ] Implement `GET /documents/:id` and `GET /documents` for basic CRUD/listing.
- [ ] Implement `POST /search` — takes a query string, embeds it, runs the pgvector similarity query, returns top-k chunks with scores.
- [ ] Add input validation (e.g. `zod`) on all request bodies.
- [ ] Write a Postman/Insomnia collection or `curl` scripts to manually test each endpoint.

**Checklist**
- [ ] Can POST a document and see it chunked + embedded + stored.
- [ ] Can POST a search query and get relevant chunks back, ranked by similarity.
- [ ] Basic request validation is in place (no unhandled malformed input crashes the server).

---

### Week 4 — Project 1: streaming RAG chat, auth, hardening, deploy

**Build**
- [ ] Implement `POST /chat` — takes a user message + conversation id, retrieves relevant chunks (RAG), assembles the context (system prompt + retrieved chunks + chat history), calls the model, and **streams** the response back (SSE or chunked HTTP) with inline citations pointing to source chunk IDs.
- [ ] Add JWT auth middleware (reuse your existing Express auth patterns) — protect all routes except health check.
- [ ] Add rate limiting (`express-rate-limit` or a Redis-backed limiter) per user/API key.
- [ ] Add retries with exponential backoff + timeouts around every model API call (don't let a hung request hang the server).
- [ ] Add structured logging (request id, latency, token usage, model used) — plain `pino`/`winston` to start, no need for a dashboard yet (that comes in Month 3).
- [ ] Write a `Dockerfile` and `docker-compose.yml` (app + Postgres with pgvector image).
- [ ] Deploy to AWS EC2: provision instance, install Docker, `docker compose up -d`, confirm endpoints reachable externally, set up basic firewall/security group rules.
- [ ] Write the README: architecture diagram (even ASCII/Mermaid is fine), setup instructions, example requests.

**Checklist**
- [ ] `/chat` streams a real answer with citations back to source chunks.
- [ ] Auth, rate limiting, retries/timeouts, and logging are all live.
- [ ] App runs in Docker locally and is deployed on EC2, reachable over the internet.
- [ ] README is complete enough that a stranger could run it.
- [ ] **Project 1 shipped.** Sunday: commit, push, post one sentence of progress publicly.

---

## Month 2 (Weeks 5–8) — Light Python + Agents + Project 2A

### Week 5 — Python basics + FastAPI + Pydantic

**Learn**
- [ ] Python syntax essentials for someone coming from JS: types/typing hints, list/dict comprehensions, `async`/`await` (very similar to JS promises), virtual envs (`venv`), package management (`pip`/`poetry`).
- [ ] `httpx` — the Python equivalent of `axios`/`fetch` for making HTTP calls (including async calls).
- [ ] **FastAPI** — routing, path/query params, request bodies, dependency injection, automatic OpenAPI docs at `/docs`. Map every concept back to its Express equivalent explicitly (e.g. `@app.post()` ≈ `app.post()`, FastAPI dependencies ≈ Express middleware).
- [ ] **Pydantic** — schema/model validation, equivalent to `zod`/Joi in the Node world.
- [ ] Explicitly skip: pandas, numpy, any ML/math library — not needed for this plan.

**Resources (free)**
- [freeCodeCamp — FastAPI Course for Beginners](https://www.classcentral.com/course/freecodecamp-fastapi-course-for-beginners-104922) — free, full crash course.
- Cursa's free Python FastAPI course (Turtle Code) — covers async, validation, OpenAPI docs, no cost.

**Build**
- [ ] Set up a Python virtual env and a minimal FastAPI app (`uvicorn main:app --reload`).
- [ ] Port 2–3 of your simple Node scripts from Week 1 to Python (call an LLM API, stream a response) — this cements the syntax fast.
- [ ] Build a toy FastAPI service with one `GET`, one `POST` with a Pydantic request model, and confirm `/docs` auto-generates correctly.
- [ ] Use `httpx.AsyncClient` to call an external API (e.g. a public REST API) from inside a FastAPI route.

**Checklist**
- [ ] Comfortable reading and writing basic Python without constantly checking syntax.
- [ ] Have a working FastAPI service with at least 2 endpoints and Pydantic validation.
- [ ] Can explain FastAPI's request lifecycle in terms of Express equivalents.

---

### Week 6 — Agents & tool calling

**Learn**
- [ ] The ReAct-style loop: Reason → Act (call a tool) → Observe (tool result) → repeat until done or max steps.
- [ ] Tool/function schemas: how you describe a tool (name, description, JSON-schema args) so the model can decide when/how to call it.
- [ ] Agent memory: short-term (conversation buffer) vs long-term (stored summaries/vector memory) — keep it conceptual, you already know how to persist state.
- [ ] **When NOT to use an agent** — a single well-crafted prompt or a deterministic pipeline is often better/cheaper/more reliable than a multi-step agent. Be able to articulate this trade-off (it's an interview-favorite question).
- [ ] Read/skim: DeepLearning.AI "Functions, Tools and Agents with LangChain."

**Resources (free)**
- [AI Agents in LangGraph — DeepLearning.AI](https://www.deeplearning.ai/courses/ai-agents-in-langgraph) — free to watch; the first half has you build an agent from scratch (matches this week), second half rebuilds it with LangGraph (matches Week 7).

**Build**
- [ ] Write a minimal agent loop by hand (no framework yet) in Node or Python: define 2 tools (e.g. `queryDatabase`, `callExternalApi`), let the model pick one, execute it, feed the result back, loop until the model returns a final answer.
- [ ] Add a max-step guard (e.g. stop after 5 iterations) so a misbehaving loop can't run forever.
- [ ] Log every step (reasoning, tool called, args, result) to the console so you can see the loop working.

**Checklist**
- [ ] Have a working hand-rolled agent loop with at least 2 tools.
- [ ] Can explain, with an example, a case where an agent is overkill and a plain API call/pipeline is better.

---

### Week 7 — Orchestration (LangGraph.js / Vercel AI SDK agents) + start Project 2A

**Learn**
- [ ] LangGraph.js (or Vercel AI SDK's built-in agent/tool-loop primitives) — how it formalizes the loop you hand-built in Week 6: nodes, edges, state, conditional routing between steps.
- [ ] Multi-step flow design: how to break a task into discrete steps with clear inputs/outputs instead of one giant prompt.

**Resources (free)**
- [AI Agents in LangGraph — DeepLearning.AI](https://www.deeplearning.ai/courses/ai-agents-in-langgraph) — same course as Week 6; this is the "rebuild with LangGraph" half.
- Great Learning's free LangGraph course — covers graph-based workflows and multi-agent patterns, no cost.

**Build (Project 2, Part A — Agentic backend service)**
- [ ] Scaffold the service (Node/Express, reusing Month 1 patterns) or FastAPI if you want extra Python reps — your call, but be consistent with what you'll extend in Month 3.
- [ ] Define the domain: pick a concrete multi-step task (e.g. "research an entity across your DB and an external API, then produce a structured report").
- [ ] Implement tool 1: a DB query tool against your MongoDB or Postgres (reuse existing data or seed sample data).
- [ ] Implement tool 2: a call to a real external API (pick something with a free tier — e.g. a public data API).
- [ ] Wire the tools into LangGraph.js / the AI SDK's agent primitive, replacing your hand-rolled loop.
- [ ] Add step-by-step logging/tracing of the agent's reasoning and tool calls (plain console/DB logging for now).

**Checklist**
- [ ] Agent successfully completes the multi-step task end-to-end using both tools.
- [ ] Framework-based loop replaces the hand-rolled version and is easier to extend.

---

### Week 8 — Async job queue (BullMQ + Redis) + finish Project 2A

**Learn**
- [ ] Why long-running agent tasks shouldn't block an HTTP request/response cycle.
- [ ] BullMQ concepts: queues, workers, jobs, retries, job status/progress.

**Build**
- [ ] Set up Redis (Docker container) + BullMQ in the project.
- [ ] Change the API shape: `POST /tasks` enqueues a job and returns a `taskId` immediately; a BullMQ worker process picks it up and runs the agent loop; `GET /tasks/:id` returns status (`pending`/`running`/`done`/`failed`) and the result once ready.
- [ ] Add job-level retry policy and error handling (a failed tool call shouldn't silently kill the whole job).
- [ ] Add basic auth + rate limiting to the API (reuse Month 1 middleware).
- [ ] Dockerize (app + worker + Redis + your DB) with `docker-compose`.
- [ ] Write the README: architecture, how the queue works, example request/response for `POST /tasks` and `GET /tasks/:id`.

**Checklist**
- [ ] Long agent runs no longer block requests — confirmed by enqueueing a task and polling for status.
- [ ] Worker retries failed jobs sensibly and surfaces failures clearly.
- [ ] Fully dockerized and running locally end-to-end.
- [ ] **Project 2 Part A shipped** (Part B — MCP refactor — comes in Month 3). Sunday: commit + progress note.

---

## Month 3 (Weeks 9–12) — MCP + Evals + Observability

### Week 9 — MCP concepts deep dive

**Learn**
- [ ] Read the official MCP spec/docs end-to-end: what problem MCP solves (standardizing how models discover/call tools and access data/resources, instead of bespoke per-app glue).
- [ ] Core primitives: **servers** (expose tools/resources/prompts), **clients** (connect to servers, e.g. inside your agent), **tools** (callable functions with schemas), **resources** (readable data, like files or DB records), **prompts** (reusable prompt templates a server can expose).
- [ ] Transport basics: stdio vs HTTP/SSE transports for MCP servers.
- [ ] Skim the `@modelcontextprotocol/sdk` (TypeScript) docs and a couple of example open-source MCP servers to see real patterns.

**Resources (free)**
- [MCP: Build Rich-Context AI Apps with Anthropic — DeepLearning.AI](https://www.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic) — taught by Anthropic's Head of Technical Education, ~1h48m, free to watch.

**Build**
- [ ] Install `@modelcontextprotocol/sdk` and run one of the official example servers locally to see the protocol in action (use the MCP Inspector tool to poke at it).
- [ ] Sketch (on paper/markdown) which of your Month 1–2 capabilities make sense as MCP tools (e.g. "query documents," "run agent task," "search chunks").

**Checklist**
- [ ] Can explain MCP's client/server/tool/resource/prompt model without notes.
- [ ] Have run and inspected at least one existing MCP server locally.

---

### Week 10 — Build an MCP server (Project 3 start)

**Build**
- [ ] Scaffold a new standalone repo for the MCP server (separate from Project 1/2 — this needs to be independently publishable).
- [ ] Using `@modelcontextprotocol/sdk`, implement the server skeleton with stdio (and/or HTTP) transport.
- [ ] Implement Tool 1: wrap a real capability, e.g. a DB query tool hitting your Postgres/Mongo (reuse Project 1/2 data).
- [ ] Implement Tool 2: wrap an internal API call (e.g. reuse Project 1's `/search` endpoint as an MCP tool).
- [ ] Implement Tool 3 (optional but recommended): a file/store lookup tool.
- [ ] Add input validation on every tool's arguments (Pydantic/zod-equivalent schema in the MCP tool definition).
- [ ] Add auth if the server exposes anything sensitive (API key or token passed via server config/env).
- [ ] Test with the MCP Inspector — confirm each tool is discoverable and callable with correct schemas.

**Checklist**
- [ ] MCP server runs locally and exposes 2–3 working tools.
- [ ] Each tool validates its inputs and returns well-formed results/errors.
- [ ] Verified working via MCP Inspector.

---

### Week 11 — Use MCP as a client + evaluation harness

**Build**
- [ ] Go back to your Month 2 agent service and replace its bespoke tool definitions with an **MCP client** connecting to your new MCP server — tools are now standardized, not inline.
- [ ] Confirm the agent still completes its multi-step task correctly, now sourcing tools via MCP.

**Learn**
- [ ] Evaluation approaches: golden test sets (input → expected output/behavior), automated scoring via **RAGAS** (for RAG-specific metrics: faithfulness, answer relevancy, context precision/recall) or **LLM-as-judge** (a second model scores the output against a rubric).

**Resources (free)**
- [Langfuse — Beginner's Guide to RAG Evaluation with Langfuse and Ragas](https://langfuse.com/guides) — free official guide covering both tools together.

**Build**
- [ ] Create a test set of 15–30 realistic queries for Project 1 (RAG) with expected answers/source docs.
- [ ] Wire up RAGAS (or a simple custom LLM-as-judge script) to score Project 1's RAG responses against this set.
- [ ] Produce a baseline score report (even a simple JSON/CSV output is fine at this stage).

**Checklist**
- [ ] Agent from Project 2 now calls tools via MCP instead of inline definitions.
- [ ] Have a repeatable eval script that scores RAG quality against a fixed test set, not "vibes."

---

### Week 12 — Observability + finish & publish Project 3

**Learn**
- [ ] Tracing concepts: spans, traces, and what to capture per LLM call (latency, token usage/cost, model, prompt version, success/failure).
- [ ] Pick a tool: **Langfuse** or **LangSmith** (hosted/open-source tracing for LLM apps) — or, consistent with "reuse your stack," a custom logger writing structured events to Postgres + a small dashboard page.

**Resources (free)**
- [PyImageSearch — RAG Observability with Langfuse, vLLM, and FAISS](https://pyimagesearch.com/2026/06/15/rag-observability-with-langfuse-vllm-and-faiss/) — free tutorial series instrumenting a RAG pipeline with tracing.
- [Langfuse guides](https://langfuse.com/guides) — official, free, includes tracing + evaluation walkthroughs.

**Build**
- [ ] Instrument Project 1 (RAG) and Project 2 (agent) calls with tracing — every model call and tool call gets a span with latency/cost/tokens.
- [ ] Build a minimal dashboard (a simple page or a few SQL queries + charts) showing: requests over time, average latency, token cost, success rate.
- [ ] Add the eval harness from Week 11 as a scheduled/manual script that logs scores over time (so you can show quality trending, not just a single run).
- [ ] Finish polishing the MCP server repo: README (what it does, install/run instructions, tool list with example calls), license, versioned `package.json`.
- [ ] Publish the MCP server (npm publish if applicable, and/or a public GitHub repo with clear instructions to run it standalone).

**Checklist**
- [ ] Tracing/observability live on at least Project 1 and Project 2.
- [ ] Dashboard shows latency, cost, and success rate at a glance.
- [ ] **MCP server published** as a standalone, documented repo — this is a standout portfolio piece.
- [ ] **Project 2 Part B + Project 3 shipped.** Sunday: commit + progress note.

---

## Month 4 (Weeks 13–16) — Production Hardening: Security, Guardrails, Cost

### Week 13 — AI security: OWASP LLM Top 10

**Learn**
- [ ] Read the OWASP Top 10 for LLM Applications end-to-end. For each item, write one sentence in your own words on what it means and one on how you'd mitigate it:
  - [ ] LLM01 Prompt Injection
  - [ ] LLM02 Insecure Output Handling
  - [ ] LLM03 Training Data Poisoning (know it conceptually — not your concern as an app-layer dev, but be able to speak to it)
  - [ ] LLM04 Model Denial of Service
  - [ ] LLM05 Supply Chain Vulnerabilities
  - [ ] LLM06 Sensitive Information Disclosure (PII/data leakage)
  - [ ] LLM07 Insecure Plugin/Tool Design
  - [ ] LLM08 Excessive Agency
  - [ ] LLM09 Overreliance
  - [ ] LLM10 Model Theft

**Resources (free)**
- [RansomLeak — 10 free OWASP LLM Top 10 exercises](https://ransomleak.com/blog/owasp-llm-top-10-training-course/) — free, no signup, hands-on exercise per category.

**Build**
- [ ] Audit Project 1 and Project 2 against this list — write a short markdown "security notes" doc per project listing which risks apply and current mitigation status.
- [ ] Fix at least one real gap you find (e.g. unescaped model output rendered somewhere, or a tool with excessive permissions).

**Checklist**
- [ ] Can explain all 10 categories without notes.
- [ ] Have a written security audit for at least one existing project with concrete findings.

---

### Week 14 — Guardrails

**Learn**
- [ ] Input validation for LLM apps: detecting/blocking obvious prompt injection patterns, length limits, content filtering.
- [ ] Output validation: schema-checking structured outputs before using them, sanitizing before rendering (XSS-equivalent risk when model output reaches a UI).
- [ ] Guardrail patterns: max-step ceilings (already partly done via agent loop limits), cost ceilings per user/session, allow/deny lists for tool actions, PII redaction (regex/NER-lite before logging or sending to the model), human-in-the-loop approval gates for risky actions.

**Resources (free)**
- No dedicated free video course for LLM guardrails specifically — this week is docs-driven. Reuse the mitigation notes from Week 13's [RansomLeak OWASP exercises](https://ransomleak.com/blog/owasp-llm-top-10-training-course/) and skim the guardrail-pattern sections of the [LiteLLM docs](https://docs.litellm.ai/docs/) (used again in Week 15).

**Build**
- [ ] Add an input guardrail middleware to Project 1/2: reject or flag suspicious inputs (basic injection heuristics, length caps).
- [ ] Add an output guardrail: validate structured outputs against schema before returning; sanitize any output rendered as HTML/markdown.
- [ ] Add a per-user cost ceiling (track cumulative token spend per user/session in Postgres/Redis; block further calls once exceeded).
- [ ] Add an allow-list for the agent's tools (explicit list of permitted actions — no dynamic/arbitrary tool execution).
- [ ] Implement a simple PII redaction step before logging request/response bodies.
- [ ] For the agent (Project 2): add a human-in-the-loop approval step for one "risky" simulated action (e.g. anything that would write/delete data) — require explicit confirmation before executing.

**Checklist**
- [ ] Input and output guardrails are live on at least one project.
- [ ] Cost ceiling enforced per user.
- [ ] PII redaction applied before logs are written.
- [ ] Agent has at least one human-in-the-loop gate for a risky action.

---

### Week 15 — AI gateway: routing + semantic caching (Project 4 start)

**Learn**
- [ ] Model routing: sending easy/cheap queries to a cheap/fast model and hard queries to a stronger model — how to classify "easy vs hard" (heuristics, or a cheap classifier call).
- [ ] Semantic caching: cache responses keyed by embedding similarity of the query (not exact string match) so near-duplicate queries hit the cache.
- [ ] Fallback strategy: what to do when a provider errors/times out (fallback to a secondary provider/model).
- [ ] Retries with backoff at the gateway level (distinct from per-request retries you already built in Month 1).
- [ ] Skim LiteLLM docs (proxy/gateway options) — decide whether to use LiteLLM or roll your own (plan default: roll your own, since it's better portfolio signal for "pure backend engineering").

**Resources (free)**
- [LiteLLM docs — Tutorials](https://docs.litellm.ai/docs/) — free, official, step-by-step on proxy setup, routing, and semantic caching. Read for concepts even though you're hand-rolling the gateway.

**Build (Project 4 — AI Gateway service)**
- [ ] Scaffold a new Express service sitting in front of 2+ model providers (e.g. Anthropic + OpenAI, or two different model tiers from one provider).
- [ ] Implement `POST /v1/chat` as the gateway's single entry point.
- [ ] Implement routing logic: a simple rule-based or cheap-model classifier decides which downstream model handles the request.
- [ ] Implement semantic cache: embed incoming queries, store in pgvector (reuse Month 1 skills) with the cached response, check for a near-match (similarity above threshold) before calling a model.
- [ ] Implement fallback: if the primary provider errors or times out, retry against the secondary provider automatically, and surface which one actually served the response.

**Checklist**
- [ ] Gateway routes between at least 2 models based on a defined rule.
- [ ] Semantic cache demonstrably returns a cached response for a paraphrased repeat query.
- [ ] Fallback to a secondary provider works when the primary is forced to fail (test by pointing at a bad endpoint/key).

---

### Week 16 — Per-user quotas, cost dashboard, finish Project 4

**Build**
- [ ] Add per-user/API-key quotas (requests/tokens per day) enforced at the gateway, reusing the cost-ceiling pattern from Week 14.
- [ ] Add a cost dashboard: track spend per user, per model, per day; expose via a simple page or `/metrics` endpoint + small chart.
- [ ] Add structured logging/tracing consistent with Month 3's observability approach (reuse Langfuse/Langfuse-alternative or your custom logger).
- [ ] (Optional/Emerging) Add basic prompt versioning: store prompts in a table/config with a version id, log which version served each request, so you could A/B test later.
- [ ] Dockerize + deploy the gateway (EC2, same pattern as Project 1).
- [ ] Write the README: architecture diagram, routing rules, caching strategy, how fallback works, example requests.

**Checklist**
- [ ] Quotas enforced and visible per user.
- [ ] Cost dashboard shows spend broken down by user/model/day.
- [ ] Gateway deployed and reachable.
- [ ] **Project 4 shipped.** Sunday: commit + progress note.

---

## Month 5 (Weeks 17–20) — Multimodal/Voice + Advanced RAG + Project 5

### Week 17 — Multimodal via API

**Learn**
- [ ] Vision models via API: sending images (base64 or URL) alongside text prompts; use cases — image description, data extraction from screenshots/scanned docs, OCR-style tasks.
- [ ] Image generation via API (optional exposure, not a focus).
- [ ] Understand this is "just a different input type to an API you already know how to call" — no new infra concepts beyond handling file uploads and larger payloads.

**Resources (free)**
- [GPT-4o Vision Guide](https://getstream.io/blog/gpt-4o-vision-guide/) and [Claude Vision API guide](https://claudeimplementation.com/blog/claude-vision-api) — free written tutorials with code, cover structured JSON extraction from images.
- machinelearningplus's Multimodal AI tutorial — free, covers GPT-4o/Claude/Gemini vision APIs, chart analysis, receipt OCR.

**Build**
- [ ] Write a script that sends an image (a screenshot or scanned PDF page) to a vision-capable model and extracts structured data (e.g. `{invoice_number, date, total}`) as JSON.
- [ ] Test with 3–4 varied documents/images to see failure modes (skewed scans, handwriting, low res).
- [ ] Decide which Project 5 track you're doing this month: **(a) multimodal document-understanding service** or **(b) voice assistant backend**. (Plan below assumes (a) as primary with (b) as the optional alternate in Week 19 — swap freely based on your interest.)

**Checklist**
- [ ] Can extract structured data from an image/PDF via a vision model API call.
- [ ] Have picked your Project 5 direction.

---

### Week 18 — Advanced RAG: hybrid search, re-ranking, chunking improvements

**Learn**
- [ ] Hybrid search: combining keyword search (Postgres full-text search / `tsvector`) with vector similarity search, then merging/re-ranking results.
- [ ] Metadata filtering: narrowing vector search by structured fields (date, source, document type) before/after the similarity search.
- [ ] Re-ranking: using a dedicated re-ranking model (e.g. Cohere Rerank) to re-order the top-N retrieved candidates by relevance before sending to the LLM.
- [ ] Better chunking: semantic/recursive chunking vs your Month 1 fixed-size approach — chunking by document structure (headings, paragraphs) instead of raw character counts.

**Resources (free)**
- DeepLearning.AI's Advanced RAG short courses (LlamaIndex/Weaviate-based) — free to watch, cover re-ranking and metadata filtering concepts; implement against Cohere Rerank's free-tier API for the actual build.

**Build**
- [ ] Add a `tsvector` column + GIN index to your `chunks` table (Project 1) for full-text search.
- [ ] Implement a hybrid query: run both keyword and vector search, merge results (e.g. reciprocal rank fusion), return combined ranked list.
- [ ] Add metadata filters to the search endpoint (e.g. filter by `document_id`, `created_after`).
- [ ] Integrate a re-ranking step (Cohere Rerank or similar) on the top-20 hybrid results, keeping the top-5 for the final context.
- [ ] Rewrite the chunker to split on semantic boundaries (headings/paragraphs) rather than fixed character windows; re-ingest a test document and compare retrieval quality using your Week 11 eval harness.

**Checklist**
- [ ] Hybrid search (keyword + vector) implemented and returning better results than vector-only on at least one test query.
- [ ] Re-ranking step live and measurably improving top results.
- [ ] Eval scores (RAGAS/LLM-judge) improved or at least documented vs the Month 1 baseline.

---

### Week 19 — Project 5 build: multimodal document service (or voice, optional)

**Build (Track A — Multimodal document-understanding service)**
- [ ] Scaffold the service: `POST /upload` (PDF/image) → store file, extract via vision model → structured extraction stored in DB.
- [ ] Implement `POST /:documentId/ask` — Q&A over the uploaded document's extracted content + original RAG pipeline for grounding.
- [ ] Handle multi-page PDFs (split into pages/images, extract per page, merge results).
- [ ] Add validation for file type/size, and graceful error handling for extraction failures.

**Build (Track B — Voice assistant backend, optional/emerging, if chosen instead)**
- [ ] Wire up speech-to-text (STT) → LLM → text-to-speech (TTS) as a pipeline, or use a realtime streaming voice API if the provider offers one.
- [ ] Implement a `/voice/session` endpoint handling audio in, streamed audio out.
- [ ] Test latency end-to-end (STT + LLM + TTS) and note where the bottleneck is.

**Checklist**
- [ ] Core Project 5 pipeline works end-to-end on at least 3 real test inputs (documents or voice sessions).

---

### Week 20 — Finish Project 5: guardrails, observability, deploy

**Build**
- [ ] Bake in the guardrails from Month 4 (input/output validation, cost ceilings) into Project 5.
- [ ] Bake in observability from Month 3 (tracing, logging, dashboard) into Project 5.
- [ ] Dockerize and deploy to AWS EC2, same pattern as prior projects.
- [ ] Write the README with architecture, setup, and example requests/responses (include a sample extracted JSON or a sample voice interaction transcript).
- [ ] (Optional/Emerging) Skim GraphRAG concepts — know at a high level when a knowledge graph beats plain vector search (e.g. multi-hop relationship queries) — no implementation required unless you want the extra depth.

**Checklist**
- [ ] Project 5 has guardrails + observability consistent with the rest of your portfolio.
- [ ] Deployed and reachable.
- [ ] **Project 5 shipped.** Sunday: commit + progress note.

---

## Month 6 (Weeks 21–24) — Self-Host, Deploy, Package, Job-Search

**Applications start this week — run this in parallel with the remaining technical work, don't wait until Week 24.**

### Week 21 — Self-hosting open models + START APPLYING

**Learn**
- [ ] Ollama: easiest path to running an open model locally/on a server — pull a model, run it, hit its local API.
- [ ] vLLM: production-grade serving — higher throughput, batching, OpenAI-compatible API server.

**Resources (free)**
- [Ollama Tutorial for Beginners (2026) — YouTube](https://www.youtube.com/watch?v=fU38n-CH7ds) — free.
- [vLLM official docs](https://docs.vllm.ai/) + DeepLearning.AI's "Fast and Efficient LLM Inference with vLLM" (free to watch) for the conceptual side.

**Build**
- [ ] Install Ollama on your EC2 instance (or locally), pull a small open model, confirm you can query it via its API.
- [ ] Stand up vLLM in Docker serving the same or a similar model, and compare basic throughput/latency against Ollama.
- [ ] (Optional) Point one existing project's gateway (Project 4) at the self-hosted model as an additional routable "provider" — proves you can run models, not just call hosted APIs.

**Job search — start now**
- [ ] Rewrite your resume headline/summary around the "Applied AI / AI-Product backend engineer" positioning from the Definition of Done.
- [ ] Update LinkedIn headline + About section with the same positioning.
- [ ] List target companies/roles (remote + India product/GCC teams per the plan's stated target market).
- [ ] Start applying — set a weekly application target (e.g. 5–10/week) and track it in a simple spreadsheet (company, role, date applied, status).

**Checklist**
- [ ] Have a self-hosted open model running and queryable via both Ollama and vLLM.
- [ ] Resume and LinkedIn updated with new positioning.
- [ ] First batch of applications sent.

---

### Week 22 — Deployment patterns + AWS certification study

**Learn**
- [ ] Deployment patterns: multi-container deploys, environment/secrets management (AWS Secrets Manager or `.env` + parameter store), basic autoscaling on AWS (target-tracking scaling policies on EC2/ECS). Kubernetes explicitly optional — skip unless you specifically want the infra/LLMOps track.
- [ ] Start AWS Certified AI Practitioner prep: go through the official exam guide section by section, focusing on GenAI/Bedrock vocabulary (this is the "fast, ATS-keyword" cert from the plan).

**Resources (free)**
- [AWS Skill Builder — AI Practitioner Exam Prep Plan](https://skillbuilder.aws/category/exam-prep/ai-practitioner) — official, completely free.
- [Coursera — AWS Certified AI Practitioner Exam Prep](https://www.coursera.org/learn/aws-certified-ai-practitioner-exam-prep) — free to audit (cert requires payment).

**Build**
- [ ] Move secrets for at least one project out of plain `.env` files into a proper secrets manager.
- [ ] Set up basic autoscaling (or document the plan/config for it) on one deployed service.
- [ ] Do daily practice questions/flashcards for the AWS cert.

**Job search**
- [ ] Continue weekly application cadence.
- [ ] Start reaching out to 2–3 people/week for informational chats or referrals (LinkedIn, alumni networks, communities).

**Checklist**
- [ ] Secrets management improved on at least one project.
- [ ] Autoscaling configured or documented.
- [ ] AWS cert study on track (aim to be ready to schedule the exam by end of week).

---

### Week 23 — AWS exam + portfolio polish

**Build**
- [ ] Sit the **AWS Certified AI Practitioner** exam.
- [ ] Polish all 5 project READMEs: consistent structure (what it does, architecture diagram, tech stack, setup, example usage, what it demonstrates).
- [ ] Add a simple architecture diagram to each repo (Mermaid diagrams in the README are fine — no design tool required).
- [ ] Confirm all 5 projects are actually live/reachable (re-deploy anything that's drifted).
- [ ] Write one short case study per project (project → problem → approach → result, 200–400 words each) for LinkedIn/portfolio site.

**Job search**
- [ ] Continue applications + networking cadence.
- [ ] Start doing mock interviews or practicing answers to the "when would you NOT use an agent," "how do you keep RAG answers grounded," "how do you control LLM costs" style questions your projects now let you answer with real examples.

**Checklist**
- [ ] AWS Certified AI Practitioner exam completed.
- [ ] All 5 project READMEs polished with diagrams.
- [ ] 5 case studies written.

---

### Week 24 — Capstone (optional) + final push

**Build (optional capstone)**
- [ ] If time allows: wire together pieces into one flagship system — e.g. a RAG + agent product that uses your published MCP server, runs behind your Project 4 AI gateway, with Month 4 guardrails, Month 3 evals/observability, and an option to route to your self-hosted model from Week 21.
- [ ] Document this as "the one system that tells your whole story" — this is your best portfolio centerpiece if you have the bandwidth.

**Wrap-up**
- [ ] Finalize resume + LinkedIn with all 5 (or 6, with capstone) projects, cert, and case studies.
- [ ] Confirm every Definition-of-Done claim below has a live link or repo backing it.
- [ ] Continue applications at full pace — this doesn't stop at Week 24, it continues until you land the role.

**Checklist — Definition of done (verify each with a link)**
- [ ] I build LLM features — RAG, agents, multimodal — on existing models. → Projects 1, 2, 5.
- [ ] I ship them as real backend services: auth, queues, guardrails, evals, observability. → All projects, esp. 1, 2, 4.
- [ ] I build MCP servers and connect agents to them with the current standard. → Project 3 (published), Project 2 client integration.
- [ ] I make AI apps cheap, safe, and reliable (gateway, caching, routing, OWASP). → Project 4, Month 4 guardrail work.
- [ ] I can self-host and deploy models when needed. → Week 21 Ollama/vLLM work.

---

## Quick-reference: what NOT to spend time on (repeated from the source plan, worth keeping visible weekly)
- Training models from scratch, deep learning theory, PyTorch/TensorFlow internals.
- Linear algebra, calculus, statistics for ML.
- Building or pre-training foundation models.
- Heavy fine-tuning / research techniques (consumer-grade fine-tuning API only, and only if time allows — not scheduled as a core week above).
- Kubernetes, unless you deliberately want to extend into the infra/LLMOps track after Week 24.

## Weekly cadence reminder
- **Weekdays (2× ~1 hr):** one learning item + one small experiment from that week's list.
- **Weekend (1× ~4–6 hr block):** the week's "Build" section / active project work.
- **Every Sunday (15 min):** commit your work + post one sentence of progress publicly. This becomes your job-search narrative and interview material by Month 6.
