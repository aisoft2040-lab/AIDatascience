# GitHub Copilot Workspace Instructions (AIDataScience)

These instructions orient AI coding agents for this repository. Current state: planning-only; single file `Ai Engineer Development Plan.txt` (v4.0). Treat this as the authoritative roadmap for forthcoming code. Keep outputs lean, actionable, and directly tied to the plan.

## 1. Repository Purpose & Roadmap
- Goal: 5‑month progression to production‑grade AI engineer portfolio (Weeks 1–20).
- Deliverables evolve weekly (FastAPI chatbot → RAG → Agents → Fine‑tuning → Portfolio → Job search).
- Each week is a self‑contained project folder (see planned tree below). Agents should create folders only when starting that week’s build work.

### Planned Top-Level Structure
```
Grok-AI-Engineer-5Months/
  01_Week1_FastAPI_Chatbot/
  02_Week2_RAG_PDF/
  03_Week3_CrewAI_Agents/
  04_Week4_Gemma1B_Finetune/
  ... (continue sequentially)
  docs/linkedin_posts/
  notes/python_math/
  README.md
```
Naming: Prefix with zero‑padded week number; use concise underscore separators; no spaces.

## 2. When Creating Code
- Always start from the week’s mission + 5 detailed items in the plan; convert each item into a subfolder `src/`, `scripts/`, or `docs/` artifact.
- Provide minimal runnable MVP first (API endpoint / Streamlit page / workflow script) before optimizations.
- Add a `README.md` inside each week folder with: Purpose, Stack, Quick Start, Demo notes (Loom link placeholder), Deployment command.
- Keep dependency specs: Use `requirements.in` + compile with `uv pip compile` → `requirements.txt` (per Week 1 principle). Do NOT pin Python to patch unless required.

## 3. Environment & Tooling
- Weeks 1–7: Target Windows 11 + WSL2 (Ubuntu). Provide PowerShell commands wrapped for WSL onboarding only when missing.
- Weeks 8–20: Assume macOS (M2/M3). Prefer cross‑platform commands (`bash` over PowerShell) unless Windows‑specific.
- Local constraints: 16GB RAM, no GPU → prefer quantized models (Q4 or below) or external inference APIs (Groq, Fireworks, Together). Avoid heavyweight local fine‑tunes >1 hour.

## 4. AI/LLM Integration Patterns
- Chatbot (Week 1): FastAPI + model fallback (local Ollama Gemma‑3‑1B → Groq API). Implement fallback as exception boundary or latency threshold.
- RAG (Week 2/5): Pipeline = Ingest (PyPDF2) → Chunk (simple text split) → Embed (choose lightweight model or API) → Vector DB (Qdrant) → Retrieve → Compose answer. Keep retrieval layer abstract (interface/module).
- Agents (Week 3/6): Multi‑agent pattern: Search → Summarize → Respond. Force JSON output by post‑processing or system prompt schema validation.
- Fine‑tuning (Weeks 4/10/14): Use LoRA/QLoRA; record hyperparams in `finetune_config.yaml`; log dataset counts. Never commit raw proprietary data—store sample schema + instructions.

## 5. Conventions
- Folder naming: `WeekX` folders use two-digit numbering.
- Scripts: Deployment scripts under `scripts/` start with action verb: `deploy_railway.sh`, `run_finetune.sh`.
- Config: Place model or RAG parameters in `config/` (YAML). Keep secrets out—reference environment variables (`GROQ_API_KEY`, etc.).
- Logging: Prefer standard logging module; INFO for major stage transitions (ingest, embed, retrieve). Avoid print spam.

## 6. Deployment & Ops
- Early deployment target: Railway (1‑click). Provide `Dockerfile` emulating minimal Python slim base + `uv` install.
- Health: Add `/health` endpoint to FastAPI apps. Return `{status: "ok", version: <git short sha>}`.
- Streamlit apps: Include `Procfile` if platform requires; keep startup command explicit.

## 7. Documentation & Portfolio Hooks
- LinkedIn posts schedule lives in plan file—agents may generate stub markdowns under `docs/linkedin_posts/` only when requested.
- Each week’s README should link forward/backward (Week N−1 / Week N+1) once those folders exist.
- Add Loom placeholders: `docs/demo_weekX.md` with sections: Setup, Walkthrough, Impact Metric.

## 8. Data Handling
- For PDFs: Store ONLY sample or anonymized files under `data/examples/`; never commit real customer content.
- Vector stores: Provide initialization script; for local dev use ephemeral directory; support override via env var `QDRANT_URL`.

## 9. Task Execution Guidance for Agents
- Parse current week from user prompt or branch name if later adopted (e.g., `week04-gemma-finetune`).
- Before generating new code: confirm absence of existing week folder → create scaffold.
- After adding code: offer run commands (WSL vs macOS if divergent).
- Keep PRs atomic per week; do not interleave modifications across multiple week folders.

## 10. What Not To Do
- Do NOT introduce unplanned frameworks (e.g., heavy orchestration) before roadmap weeks specify (LangGraph only Week 9).
- Avoid speculative optimization (vector compression, advanced retrievers) unless explicitly requested.
- Do not fabricate datasets—use schema examples.

## 11. Next Steps (Initial State)
- Week 1 scaffold not yet created: first action is to generate `01_Week1_FastAPI_Chatbot/` with minimal FastAPI + fallback stub.
- Confirm with user before initializing multi-week folder explosion; create incrementally.

---
If any section lacks clarity or you need deeper patterns after code arrives, request incremental refinement. Provide deltas, not full rewrites, on updates.
