# GitHub Copilot Workspace Instructions (AIDataScience)

These instructions orient AI coding agents for this repository.
Current state: planning and early scaffold. Treat `Ai Engineer Development Plan.txt` (v4.0) as the authoritative roadmap. Focus outputs on small, testable MVPs that follow the weekly structure.

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

## 2. When Creating Code (practical rules)
- Always start from the week’s mission + 5 detailed items in the plan; convert each item into a subfolder `src/`, `scripts/`, or `docs/` artifact. Example: Week 1 uses `Grok-AI-Engineer-5Months/01_Week1_FastAPI_Chatbot/src` for app code, tests in `tests/`.
- Provide minimal runnable MVP first (API endpoint / Streamlit page / workflow script) before optimizations. For example, `src/main.py` in Week 1 implements `/health` and `/echo` endpoints and has two `pytest` testcases in `tests/test_main.py`.
- Add a `README.md` inside each week folder with: Purpose, Stack, Quick Start, Demo notes (Loom link placeholder), Deployment command.
- Keep dependency specs: Use `requirements.in` + compile with `uv pip compile` → `requirements.txt` (per Week 1 principle). Do NOT pin Python to patch unless required.

## 3. Environment & Tooling — quick commands
- Weeks 1–7: Target Linux Mint (Ubuntu/Debian based). Provide `apt`/`bash` commands for Linux Mint environment. Prefer `bash` for examples by default.
- Weeks 8–20: Assume macOS (M2/M3). Prefer cross‑platform commands (`bash` over PowerShell) unless Windows‑specific.
- Local constraints: 16GB RAM, no GPU → prefer quantized models (Q4 or below) or external inference APIs (Groq, Fireworks, Together). Avoid heavyweight local fine‑tunes >1 hour.
  Example developer commands used in this repo:
  - Setup venv (bash):
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
  - If `pip-tools` is used to manage constraints:
    ```bash
    pip install pip-tools
    pip-compile requirements.in
    pip install -r requirements.txt
    ```
  - Run tests:
    ```bash
    pytest -q
    ```
  - Start dev server (Week 1 FastAPI):
    ```bash
    source .venv/bin/activate
    python -m uvicorn src.main:app --reload --port 8000
    curl http://localhost:8000/health
    ```

## 4. AI/LLM Integration Patterns — repo examples
- Chatbot (Week 1): FastAPI + model fallback (local Ollama Gemma‑3‑1B → Groq API). Implement fallback as exception boundary or latency threshold.
- RAG (Week 2/5): Pipeline = Ingest (PyPDF2) → Chunk (simple text split) → Embed (choose lightweight model or API) → Vector DB (Qdrant) → Retrieve → Compose answer. Keep retrieval layer abstract (interface/module). Example: `Grok-AI-Engineer-5Months/02_Week2_RAG_PDF/` contains an evaluation harness and notebook; extend `src/ingest` or `src/embeddings` when adding implementations.
- Agents (Week 3/6): Multi‑agent pattern: Search → Summarize → Respond. Force JSON output by post‑processing or system prompt schema validation.
- Fine‑tuning (Weeks 4/10/14): Use LoRA/QLoRA; record hyperparams in `finetune_config.yaml`; log dataset counts. Never commit raw proprietary data—store sample schema + instructions.

## 5. Conventions & patterns to preserve
- Folder naming: `WeekX` folders use two-digit numbering.
- Scripts: Deployment scripts under `scripts/` start with action verb: `deploy_railway.sh`, `run_finetune.sh`.
- Config: Place model or RAG parameters in `config/` (YAML). Keep secrets out—reference environment variables (`GROQ_API_KEY`, etc.). Use `.env.example` as the template and do not commit `.env`.
- Logging: Prefer standard logging module; INFO for major stage transitions (ingest, embed, retrieve). Avoid print spam.

## 6. Deployment & Ops — repo specifics
- Early deployment target: Railway (1‑click). Provide `Dockerfile` emulating minimal Python slim base + `uv` install.
- Health: Add `/health` endpoint to FastAPI apps. Return `{status: "ok", version: <git short sha>}` — Week 1 skeleton uses `APP_VERSION` environment variable; set `APP_VERSION` in `.env` to test.
- Streamlit apps: Include `Procfile` if platform requires; keep startup command explicit.

## 7. Documentation & Portfolio Hooks
- LinkedIn posts schedule lives in plan file—agents may generate stub markdowns under `docs/linkedin_posts/` only when requested. Drafts may be compiled into weekly `docs/wordpress_course/` chapters for the free WordPress course.
- Each week’s README should link forward/backward (Week N−1 / Week N+1) once those folders exist.
- Add Loom placeholders: `docs/demo_weekX.md` with sections: Setup, Walkthrough, Impact Metric.

## 8. Data Handling
- For PDFs: Store ONLY sample or anonymized files under `data/examples/`; never commit real customer content.
- Vector stores: Provide initialization script; for local dev use ephemeral directory; support override via env var `QDRANT_URL`.

## 9. Task Execution Guidance for Agents (how to be useful here)
- Parse current week from user prompt or branch name if later adopted (e.g., `week04-gemma-finetune`). When adding code, return a short demo command block showing how to run the app & tests for manual verification.
- Before generating new code: confirm absence of existing week folder → create scaffold.
- After adding code: offer run commands (Linux Mint vs macOS if divergent).
- Keep PRs atomic per week; do not interleave modifications across multiple week folders. Each PR should update `README.md` in the week folder and `requirements.in` as needed, and use the PR template `templates/PR_TEMPLATE.md`.

## 10. Developer workflows & examples (explicit)
- Quick start: create a branch, add small change, run tests locally, update `README` and `requirements.in`, open PR with the template. Example commands:
  ```bash
  git checkout -b week1/add-csv-util
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  pytest -q
  git add . && git commit -m "feat(week1): add csv util" && git push --set-upstream origin HEAD
  ```
- Run full dev web app:
  ```bash
  python -m uvicorn src.main:app --reload --port 8000
  curl -s http://localhost:8000/health | jq .
  curl -X POST http://localhost:8000/echo -H "Content-Type: application/json" -d '{"message":"hi"}'
  ```

## 11. Integration points & externals you may need to know
- Dockerfile: Week 1 includes a `Dockerfile`; use `docker build -t aiweek1:latest .` and check `scripts/deploy_railway.sh` for Railway deployment steps.
- Vector DB / embeddings: planned Qdrant example in Week 2. Use `QDRANT_URL` in `config/` when adding connectors.
- Model fallbacks: Week 1 and roadmap mention Ollama (local) -> Groq (API) fallback pattern. Implement fallback logic with timeouts so tests avoid network calls (mock skill calls in unit tests).

## 12. Tests & validation patterns
- Unit tests in this repository prefer lightweight `pytest` tests that exercise core functions and FastAPI endpoints via `TestClient` (see `tests/test_main.py`).
- Validation: When adding agents, include JSON schema validation tests to ensure output shape (see `docs/functional-spec-ai-engineer-journey.md` for policy on JSON enforcement).

If anything in this short guide is unclear or you want me to expand a section (for example: add a sample `config/` YAML template, or a CI Github Actions pipeline), say which piece should be expanded and I'll update it.

## 10. What Not To Do
- Do NOT introduce unplanned frameworks (e.g., heavy orchestration) before roadmap weeks specify (LangGraph only Week 9).
- Avoid speculative optimization (vector compression, advanced retrievers) unless explicitly requested.
- Do not fabricate datasets—use schema examples.

## 11. Next Steps (Initial State)
- Week 1 scaffold not yet created: first action is to generate `01_Week1_FastAPI_Chatbot/` with minimal FastAPI + fallback stub.
- Confirm with user before initializing multi-week folder explosion; create incrementally.

---
If any section lacks clarity or you need deeper patterns after code arrives, request incremental refinement. Provide deltas, not full rewrites, on updates.
