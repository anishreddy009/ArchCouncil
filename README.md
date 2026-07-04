# ArchCouncil

**A multi-agent debate system for technical architecture decisions.**

ArchCouncil spins up multiple LLM agents with opposing incentives (Performance, Security, Cost, Maintainability, and a Devil's Advocate) to debate real technical decisions — grounded in your own codebase/docs and live web evidence — and converges on a structured recommendation with a formal Architecture Decision Record (ADR). Over time, it logs real-world outcomes of past decisions and uses that feedback to calibrate which arguments/agents were historically reliable.

Unlike single-agent chatbots or RAG Q&A tools, this project is built around **multi-agent adversarial reasoning, citation-enforced guardrails, and outcome-based evaluation** — a genuinely underexplored pattern applied to a real engineering problem.

---

## Why this project

Most AI engineering portfolio projects are single-agent wrappers around an LLM API. ArchCouncil is designed to force hands-on experience with nearly the full AI engineering skill set:

- Multi-agent orchestration (not just single-call prompting)
- RAG grounded in real technical documents
- Tool use (web search, retrieval)
- Structured output enforcement
- Guardrails (mandatory citations, hallucination rejection)
- Long-term memory and feedback loops
- Custom evaluation harnesses
- Full observability of multi-agent traces
- Async production-style backend design

---

## Architecture Overview

```
                        ┌─────────────────────┐
                        │   User / Frontend    │
                        │ (Streamlit / React)  │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │     FastAPI Layer     │
                        └──────────┬───────────┘
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                     ▼
      ┌─────────────────────┐              ┌─────────────────────┐
      │   LangGraph Debate    │◄────────────┤   Model Router Layer  │
      │   State Machine       │             │ (Groq / Gemini /      │
      │ (5 agent personas,    │             │  OpenRouter / Ollama) │
      │  round-based turns)   │             └─────────────────────┘
      └──────────┬───────────┘
                 │
   ┌─────────────┼──────────────┐
   ▼             ▼              ▼
┌────────┐  ┌──────────┐  ┌───────────────┐
│  RAG   │  │  Web      │  │  Citation /    │
│ (Chroma│  │  Search   │  │  Guardrail     │
│/Qdrant)│  │ (Tavily)  │  │  Validator     │
└────────┘  └──────────┘  └───────────────┘
                 │
                 ▼
      ┌─────────────────────┐
      │  PostgreSQL           │
      │ (decisions, debates,  │
      │  outcomes, ADRs)      │
      └──────────┬───────────┘
                 │
                 ▼
      ┌─────────────────────┐
      │  Eval Harness +       │
      │  Langfuse Tracing     │
      └─────────────────────┘
```

---

## 6-Week Roadmap

### Week 1 — Core Debate Loop (No RAG Yet)
- [ ] Define 5 agent personas with distinct system prompts (Performance, Security, Cost, Maintainability, Devil's Advocate)
- [ ] Build a basic 2-agent debate loop in LangGraph — get coherent disagreement working before adding complexity
- [ ] Set up model router abstraction (Groq primary, OpenRouter/Ollama fallback)
- [ ] Basic FastAPI endpoint to submit a decision question and get a raw debate transcript

**Milestone:** Two agents can argue about a simple technical question in multiple rounds without crashing or repeating themselves.

### Week 2 — RAG Grounding + Citation Guardrail
- [ ] Set up Chroma (or Qdrant) vector store
- [ ] Ingest sample codebase docs / past ADRs / architecture docs for retrieval
- [ ] Integrate embedding model (sentence-transformers, local/free)
- [ ] Build citation-enforcement layer: reject/retry any agent claim without a grounding source
- [ ] Wire RAG retrieval into each agent's reasoning step

**Milestone:** Agents cite real retrieved evidence, and ungrounded claims get flagged/rejected.

### Week 3 — Full 5-Agent Orchestration + ADR Generation
- [ ] Expand to full 5-agent round-based debate with convergence detection logic
- [ ] Integrate web search tool (Tavily or similar) for live external evidence
- [ ] Structured output enforcement via Pydantic/Instructor (trade-off matrix, confidence score, recommendation)
- [ ] Auto-generate formal ADR document (Markdown → optionally exported via python-docx/Pandoc)
- [ ] Persist decisions, transcripts, and ADRs to PostgreSQL

**Milestone:** End-to-end flow — submit a question, get a full debate transcript + polished ADR output.

### Week 4 — Evaluation Harness
- [ ] Build custom eval suite (pytest-style):
  - Citation accuracy (% of claims properly grounded)
  - Debate consistency (same input → similar output across runs)
  - Convergence quality (does debate actually resolve, or loop endlessly?)
- [ ] Optionally integrate Ragas for supplementary RAG-specific metrics
- [ ] Add CI pipeline (GitHub Actions) to run eval suite on prompt/logic changes

**Milestone:** You can quantitatively say "this version of the system is X% better than the last" — not just eyeball it.

### Week 5 — Observability + Deployment
- [ ] Integrate Langfuse for full multi-agent trace logging and debugging
- [ ] Add Redis caching layer (dedupe RAG lookups, track rate limits across providers)
- [ ] Containerize with Docker Compose (FastAPI + Postgres + Redis + Chroma/Qdrant)
- [ ] Deploy to Render/Railway (or run fully local) for a live demo
- [ ] Build Streamlit (or React) frontend: debate transcript viewer, ADR display, decision history browser

**Milestone:** A shareable, deployed demo with full traceability of every debate.

### Week 6 (Stretch) — Outcome Tracking + Feedback Calibration
- [ ] Build outcome-logging feature: after a real decision plays out, log what actually happened
- [ ] Design a simple weighted-scoring recalibration (which personas/arguments were historically more accurate)
- [ ] Stretch: explore a lightweight preference-tuning pass (DPO-style) using accumulated outcome data
- [ ] Write up final architecture doc + demo video + polish README

**Milestone:** The system doesn't just debate — it gets measurably better calibrated over time based on real outcomes.

---

## Team Split Suggestion

**Person A — Debate Engine & Orchestration**
- LangGraph state machine, persona design, convergence logic
- Citation-enforcement guardrail
- Observability instrumentation (Langfuse)

**Person B — Knowledge & Evaluation Layer**
- RAG pipeline (ingestion, embedding, retrieval) + web search integration
- Outcome tracking system
- Eval harness design and CI integration
- ADR document generation

**Together**
- Model router + fallback logic
- Feedback/calibration loop (Week 6 stretch)
- Deployment and final polish

---

## Tech Stack

| Layer | Tools |
|---|---|
| LLM Providers | Groq, Google AI Studio (Gemini Flash), Ollama (local), OpenRouter |
| Agent Orchestration | LangGraph, LangChain (utility chains) |
| RAG / Retrieval | Chroma or Qdrant, sentence-transformers, Tavily (web search) |
| Structured Output / Guardrails | Pydantic, Instructor, custom citation validator |
| Backend | FastAPI, PostgreSQL, Celery/BackgroundTasks, Redis |
| Evaluation & Observability | Langfuse, custom pytest-style eval harness, Ragas (optional) |
| Document Generation | python-docx or Markdown → Pandoc |
| Frontend | Streamlit (MVP) or React |
| Deployment | Docker, Docker Compose, Render/Railway |
| CI/CD | GitHub Actions (gate on eval scores) |

---

## Getting Started

```bash
# Clone the repo
git clone <your-repo-url>
cd archcouncil

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in: GROQ_API_KEY, GOOGLE_API_KEY, TAVILY_API_KEY, DATABASE_URL, etc.

# Run local services (Postgres, Redis, Chroma)
docker compose up -d

# Run the FastAPI backend
uvicorn app.main:app --reload

# Run the frontend (if using Streamlit)
streamlit run frontend/app.py
```

---

## Project Status

🚧 In active development — see the roadmap above for current milestone.

## License

MIT (or your preferred license)
