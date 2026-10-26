# Theory to Learn — Concept Checklist (All 24 Weeks)

Every **concept** you need to *understand* across the plan, extracted from the "Learn" sections of [detail-plan.md](detail-plan.md), in order. This is the **read/understand** list — the "type/run/build" steps stay in the detail plan.

**How to use:** tick a box only when you can explain it *in your own words* (that's the interview bar). One line each is the "what it is" — go deeper via the plan's linked resources when a box won't tick.

Legend: **[Core]** = must know · **[Opt]** = optional/emerging, skip if busy.

---

## Month 1 — LLM Fundamentals + RAG + pgvector

### Week 1 — LLM fundamentals
- [ ] **Tokens & tokenization** [Core] — text is split into tokens (not words); drives cost and context limits.
- [ ] **Context window** [Core] — the max tokens a model can "see" at once; what happens when you exceed it (truncation/error) and why stuffing everything in doesn't scale.
- [ ] **Temperature** [Core] — randomness knob; 0 = deterministic, higher = more varied.
- [ ] **Sampling params: top_p, max_tokens** [Core] — other output controls (nucleus sampling, response length cap).
- [ ] **Embeddings** [Core] — text → vector of meaning; similar texts land close together (cosine similarity).
- [ ] **Structured / JSON output** [Core] — forcing valid JSON out of a model (response_format / tool-forced / schema-constrained).
- [ ] **Function / tool calling (basics)** [Core] — model returns "call this function with these args" instead of prose.
- [ ] **Streaming** [Core] — SSE / chunked responses; why it improves *perceived* latency.
- [ ] **Cost & latency** [Core] — read provider pricing; compute cost per 1K requests for a typical prompt+completion.

### Week 2 — Prompt/context engineering + RAG architecture
- [ ] **System vs user prompts vs few-shot** [Core] — which lever to pull when.
- [ ] **Context assembly** [Core] — how a real app builds the final prompt (system + retrieved docs + history + query) and orders/truncates it.
- [ ] **Prompt templates & versioning** [Core] — treat prompts like config, not hardcoded strings.
- [ ] **RAG architecture end-to-end** [Core] — chunking → embedding → vector search → retrieval → re-ranking → citation.
- [ ] **Chunking strategies** [Core] — fixed-size, sentence-aware, recursive; the small-vs-big trade-off.
- [ ] **Vector search (ANN / cosine)** [Core] — approximate nearest-neighbor search over embeddings.
- [ ] **Citation / attribution** [Core] — tracing an answer back to its source chunks.
- [ ] **pgvector fundamentals** [Core] — `vector` column type, distance operators (`<->` L2, `<=>` cosine), index types (`ivfflat` vs `hnsw`).

---

## Month 2 — Light Python + Agents

### Week 5 — Python + FastAPI + Pydantic
- [ ] **Python essentials (for a JS dev)** [Core] — typing hints, comprehensions, `async`/`await`, `venv`, `pip`/`poetry`.
- [ ] **`httpx`** [Core] — Python's `axios`/`fetch` (sync + async HTTP).
- [ ] **FastAPI** [Core] — routing, params, request bodies, dependency injection, auto OpenAPI `/docs`; map each to its Express equivalent.
- [ ] **Pydantic** [Core] — schema/model validation (the `zod`/Joi of Python).
- [ ] *(Skip: pandas, numpy, ML/math libs.)*

### Week 6 — Agents & tool calling
- [ ] **ReAct loop** [Core] — Reason → Act (call tool) → Observe (result) → repeat until done/max-steps.
- [ ] **Tool / function schemas** [Core] — name + description + JSON-schema args so the model knows when/how to call.
- [ ] **Agent memory** [Core] — short-term (conversation buffer) vs long-term (summaries / vector memory).
- [ ] **When NOT to use an agent** [Core] — a single prompt or deterministic pipeline is often better/cheaper/safer. *(Interview favorite.)*

### Week 7 — Orchestration
- [ ] **LangGraph.js / AI SDK agent primitives** [Core] — nodes, edges, state, conditional routing; formalizes the hand-built loop.
- [ ] **Multi-step flow design** [Core] — break a task into discrete steps with clear I/O instead of one giant prompt.

### Week 8 — Async job queue
- [ ] **Why long tasks shouldn't block HTTP** [Core] — request/response cycle vs background work.
- [ ] **BullMQ concepts** [Core] — queues, workers, jobs, retries, job status/progress.

---

## Month 3 — MCP + Evals + Observability

### Week 9 — MCP concepts
- [ ] **What problem MCP solves** [Core] — a standard way for models to discover/call tools & access data, instead of bespoke glue.
- [ ] **MCP primitives** [Core] — **servers**, **clients**, **tools**, **resources** (readable data), **prompts** (reusable templates).
- [ ] **MCP transports** [Core] — stdio vs HTTP/SSE.

### Week 11 — Evaluation
- [ ] **Golden test sets** [Core] — input → expected output/behavior, the basis of repeatable eval.
- [ ] **RAGAS metrics** [Core] — faithfulness, answer relevancy, context precision/recall.
- [ ] **LLM-as-judge** [Core] — a second model scores output against a rubric.

### Week 12 — Observability
- [ ] **Tracing concepts** [Core] — spans, traces; what to capture per call (latency, tokens/cost, model, prompt version, success/failure).
- [ ] **Tooling choice** [Core] — Langfuse / LangSmith vs a custom Postgres logger + dashboard.

---

## Month 4 — Security, Guardrails, Cost

### Week 13 — OWASP LLM Top 10
- [ ] **LLM01 Prompt Injection** [Core]
- [ ] **LLM02 Insecure Output Handling** [Core]
- [ ] **LLM03 Training Data Poisoning** [Core] — conceptual only (not app-layer, but be able to speak to it).
- [ ] **LLM04 Model Denial of Service** [Core]
- [ ] **LLM05 Supply Chain Vulnerabilities** [Core]
- [ ] **LLM06 Sensitive Information Disclosure (PII leakage)** [Core]
- [ ] **LLM07 Insecure Plugin/Tool Design** [Core]
- [ ] **LLM08 Excessive Agency** [Core]
- [ ] **LLM09 Overreliance** [Core]
- [ ] **LLM10 Model Theft** [Core]
- [ ] *(Bar: one sentence "what it is" + one sentence "how I'd mitigate" per item.)*

### Week 14 — Guardrails
- [ ] **Input validation for LLMs** [Core] — injection-pattern detection, length limits, content filtering.
- [ ] **Output validation** [Core] — schema-check structured output; sanitize before rendering (XSS-equivalent risk).
- [ ] **Guardrail patterns** [Core] — max-step ceilings, cost ceilings, allow/deny lists, PII redaction, human-in-the-loop gates.

### Week 15 — AI gateway
- [ ] **Model routing** [Core] — cheap model for easy queries, strong for hard; how to classify easy vs hard.
- [ ] **Semantic caching** [Core] — cache keyed by embedding similarity, not exact string match.
- [ ] **Fallback strategy** [Core] — what to do when a provider errors/times out.
- [ ] **Gateway-level retries with backoff** [Core] — distinct from per-request retries.

### Week 16
- [ ] **Prompt versioning / A-B** [Opt] — store prompts with a version id; log which version served each request.

---

## Month 5 — Multimodal + Advanced RAG

### Week 17 — Multimodal via API
- [ ] **Vision models via API** [Core] — sending images (base64/URL) with text; description, extraction, OCR-style tasks.
- [ ] **Image generation via API** [Opt] — awareness only.
- [ ] **Mental model** [Core] — it's "just a different input type" to an API you already call.

### Week 18 — Advanced RAG
- [ ] **Hybrid search** [Core] — combine keyword (Postgres `tsvector`) + vector search, then merge/re-rank (e.g. reciprocal rank fusion).
- [ ] **Metadata filtering** [Core] — narrow by structured fields (date, source, type) before/after similarity search.
- [ ] **Re-ranking** [Core] — a dedicated model (e.g. Cohere Rerank) re-orders top-N candidates before the LLM sees them.
- [ ] **Better chunking** [Core] — semantic/recursive/structure-aware vs fixed-size.

### Week 20
- [ ] **GraphRAG / knowledge graphs** [Opt] — concept only; when a graph beats plain vector search (multi-hop relationship queries).

---

## Month 6 — Self-Host + Deploy + Cert

### Week 21 — Self-hosting open models
- [ ] **Ollama** [Core] — easiest path to run an open model and hit its local API.
- [ ] **vLLM** [Core] — production serving: throughput, batching, OpenAI-compatible API.

### Week 22 — Deployment + cert
- [ ] **Deployment patterns** [Core] — multi-container deploys, secrets management (AWS Secrets Manager / parameter store), basic autoscaling.
- [ ] **Kubernetes** [Opt] — skip unless you want the infra/LLMOps track.
- [ ] **AWS Certified AI Practitioner vocab** [Core] — GenAI/Bedrock terminology, exam-guide section by section.

### Optional / emerging (whole plan)
- [ ] **Consumer-grade fine-tuning via API** [Opt] — calling a provider's fine-tune endpoint to specialize tone/format. API only — no training theory, no math.

---

## The "explain it cold" list (interview must-haves)
If you can't explain these without notes, keep studying that box:
tokens · context window · temperature · embeddings · JSON mode · function calling · streaming · **RAG pipeline end-to-end** · chunking trade-offs · **when NOT to use an agent** · MCP primitives · RAGAS vs LLM-as-judge · prompt injection + mitigation · semantic caching · model routing · hybrid search + re-ranking.

## What NOT to learn (stay out of these — deliberate boundary)
Training from scratch · deep-learning theory · PyTorch/TensorFlow internals · linear algebra/calculus/stats for ML · pre-training foundation models · heavy/research fine-tuning.
