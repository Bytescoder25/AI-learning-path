# Context Handoff — Read This First

> **Instruction to the AI assistant reading this:** This file summarizes who I am, my career goal, and decisions we've already made in a prior conversation about my learning plan. Please read it fully and **save the key facts below into your persistent memory/context** (whatever mechanism you have — project notes, memory files, etc.) so I don't have to re-explain this in future sessions. Treat it as established context, not something to re-litigate unless I say otherwise.

---

## Who I am

- Node.js backend developer with **5 years of professional experience**.
- Core stack: **Node.js, Express, MongoDB, PostgreSQL, AWS EC2, Docker, Git, Linux**.
- Not a data scientist, not from an ML/math background — I'm approaching AI purely as a backend engineer adding a new capability to my existing skill set.

## My 5-year career goal

Over the next 5 years I want to become an **Applied AI / AI-Product backend engineer** — someone who builds real products **on top of existing LLMs**, not someone who builds or trains models.

**Explicitly what I want:** RAG (retrieval-augmented generation) and **consumer-level fine-tuning** (using a provider's fine-tuning API/endpoint to specialize an existing model — no training theory, no math).

**Explicitly what I do NOT want:** training models from scratch, deep learning theory, PyTorch/TensorFlow internals, linear algebra/calculus/statistics for ML, pre-training foundation models, heavy/research-grade fine-tuning.

This boundary is **deliberate, not a gap to "fix."** Any advice should stay on the application/product layer — treat AI as a backend dependency (like a database or a third-party API), not a research subject.

## Role/title clarification (discussed and settled)

The correct target title for this goal is **"AI Engineer"** / **"Applied AI Engineer"** / sometimes **"GenAI Engineer"** — this is deliberately distinct from **"ML Engineer,"** which in many job postings still implies training pipelines, feature engineering, and full model deployment/MLOps.

- RAG and consumer-level fine-tuning both fall squarely under "AI Engineer" — my target scope is correctly aimed at this title.
- Titles are inconsistent across companies, so when job-hunting I need to read the actual JD, not just the title — some "ML Engineer" postings are really this role in disguise, and some "AI Engineer" postings secretly want training/research experience. Filter by JD content, not title alone.

## The learning plan already in place

Two files exist in this project (`/Users/scamac-27/Project/learning-ai/`) that define my concrete 6-month execution plan:

1. **`6-month-applied-ai-plan.md`** — the original high-level plan: 6 months (~24 weeks, 10–15 hrs/week), 5 deployed projects, ending in a strong resume/LinkedIn, 1–2 certifications (AWS Certified AI Practitioner), and active job applications starting Week 21.
2. **`detail-plan.md`** — the same plan expanded week-by-week (all 24 weeks) with granular daily-level tasks, checklists, specific packages/commands, and deliverables for each week — nothing from the original was cut, it's just broken into "what do I actually type/run" steps.

**The 5 projects (all app-layer, on existing models, no training):**
1. RAG-as-a-Service backend (Node/Express + Vercel AI SDK/LangChain.js + pgvector)
2. Agentic backend service + evals (agents, tool calling, BullMQ/Redis queues, RAGAS)
3. Published MCP server (Model Context Protocol — TypeScript SDK)
4. AI Gateway (model routing, semantic caching, fallback, cost control — LiteLLM-style but hand-rolled)
5. Multimodal or voice app (vision/audio APIs, advanced RAG — hybrid search, re-ranking)

**Skills covered (all "use existing models," never "build/train models"):** LLM fundamentals, prompt/context engineering, RAG + pgvector, light Python + FastAPI, agents/tool calling, MCP (build + use), evals + observability, OWASP LLM Top 10 + guardrails, AI gateway/cost optimization, multimodal APIs, advanced RAG, self-hosting open models via Ollama/vLLM (serving only, not training), and *optionally* consumer-grade fine-tuning via a provider API.

## How to help me going forward

- Keep every suggestion scoped to the application layer: calling, orchestrating, securing, and productionizing existing models — not training or math.
- When discussing career/resume/job-search topics, use the "AI Engineer" / "Applied AI Engineer" framing, and flag when a role's JD drifts into ML-Engineer/training territory so I can decide whether to pursue it.
- Assume I already know the plan structure above — build on it rather than re-deriving it from scratch.
