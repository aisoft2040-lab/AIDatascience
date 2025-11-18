# AI Engineer Journey – Functional Specification

Last updated: 2025-11-17

## 1) Purpose
- Build a 20-week, production-oriented AI Engineer portfolio (Weeks 1–20) with weekly, self-contained deliverables and measurable quality/cost/safety.
- Additionally: Create and document a foundational learning curriculum on the personal blog ("AI Engineer"), intended to serve as a practical, beginner-friendly guideline for future AI Engineer aspirants.
- Optimize for low-cost, safe integration of LLM features into existing SaaS/enterprise contexts, emphasizing evaluation, observability, and governance.

## 2) Scope
- In: Week 0(Prelearning) preparation; Weeks 1–20 implementation; evaluation & monitoring; deployment (local + Railway); documentation & English ramp-up; hiring-facing portfolio artifacts.
- Out: Heavy infra (Kubernetes/Kubeflow), large GPU training, multi-cloud orchestration beyond project needs.

## 3) Stakeholders & Users
- Primary: Project owner (you). Secondary: Aspiring AI Engineers (blog audience). Tertiary: Reviewers (interviewers/hiring managers).

## 4) Constraints
- OS & Hardware: Weeks 1–7 Linux Mint (Ubuntu/Debian); Weeks 8–20 macOS(M2/M3); 16GB RAM; no GPU.
- Budget: Prefer local/Ollama Q4 or API fallback; fine-tuning via low-cost cloud sessions ($30 total target across plan).
- Time: 6 hours/day, Sat 3h, Sun rest; LinkedIn cadence adjusted later if needed.

## 5) Success Metrics (KPI)
- Quality: Retrieval Recall@5, JSON validity rate, factuality/error rate.
- Performance/Cost: p50/p95 latency, token cost per session, cache hit rate.
- Delivery: Week deliverables completed, health endpoint present, tests pass.
- Documentation: Weekly README completeness, blog posts cadence, clarity of runbooks.

## 6) High-Level Timeline (Key Weeks)
- Week 0 (Prelearning): Python/Pandas/ML basics; Data Analytics (Excel/SQL/Tableau); integration drills; appendix for Day1 focus and 12/09 readiness.
- Week 1 (updated): FastAPI + Ollama; Groq fallback; Docker; Pytest unit tests; .env security + secret scan; input validation & error logging; Railway deploy.
- Week 2 (updated): RAG PDF; Qdrant; cosine search; Streamlit UI; Evaluation module (Precision/Recall/F1, Retrieval@k) + metric logging (latency/token/hit rate).
- Week 3 (updated): CrewAI agents; JSON schema enforcement; GitHub Actions CI/CD (lint/test/build); Prompt evaluation via JSON test cases & schema validation.
- Week 4 (updated): Gemma-1B LoRA; MLflow experiment tracking (hyperparams/metrics/model versions).
- Week 5: SME Project 1 (RAG+Streamlit, deploy/demo).
- Week 5.5 (new): Classical ML & EDA sprint (profiling; LogReg vs XGBoost; interpretation; comparison report).
- Week 6–7: SME Projects 2–3; Vision (PDF+image); deploy/demo.
- Week 8: Mac switch; environment migration.
- Week 9 (updated): LangGraph workflow; pre-added monitoring (latency/error rate/hit rate) + Responsible AI checklist (PII redaction, prompt-injection guard, audit logs).
- Week 10–14: Advanced fine-tuning, long context, quantization; evaluation automation.
- Week 15–20: Monitoring dashboard; portfolio assembly; job search.

## 7) Repository Architecture & Conventions
- Structure (planned): `Grok-AI-Engineer-5Months/XX_WeekY_*` per week; create just-in-time.
- Per week folder: `src/`, `scripts/`, `config/`, `docs/`, `requirements.in` → compile with `uv` to `requirements.txt`.
- Health endpoint: `/health`→ `{status:"ok", version:"<git_short_sha>"}`.
- Logging: Python `logging` at INFO for stage transitions (ingest/embed/retrieve).
- Secrets: `.env` + `.env.example`; no secrets committed; secret scan before deploy.

## 8) Core Solution Patterns
- Chatbot (Week 1): FastAPI + local Ollama Gemma‑3‑1B; fallback to Groq on exception/timeout; JSON schema validation for stability.
- RAG (Week 2/5): Ingest(PyPDF2) → chunk(simple split) → embed(lightweight or API) → vector DB(Qdrant) → retrieve(top‑k) → compose; evaluation harness for Precision/Recall/F1, Retrieval@k.
- Agents (Week 3/6): Search → Summarize → Respond; enforce JSON via schema + post-processing; CI/CD checks.
- Fine-tuning (Weeks 4/10/14): LoRA/QLoRA; MLflow logging; track datasets and hyperparameters.

## 9) Critical Workflows
- Dependencies: `requirements.in` compiled by `uv` to `requirements.txt`; venv per week.
- Testing: `pytest` minimal green suite (6–10 tests) targeting chunking/cosine/file IO, and fast API handlers.
- CI/CD: GitHub Actions (lint/test/build; optional docker build); regression suite for prompt/JSON validity.
- Experiment tracking: MLflow for fine-tuning weeks, simple CSV/markdown for early weeks.
- Deployment: Docker + Railway; feature flag for LLM endpoints; rollback path.

## 10) Security & Governance
- Input filter (length/charset), prompt-injection guard, PII redaction/masking.
- JSON schema validators; source grounding (top chunks) in responses.
- Audit logs: decisions/versions/sources; secure handling of documents.

## 11) Monitoring & Evaluation
- Metrics captured: latency(p50/p95), token cost/session, cache hit, Retrieval@k, JSON validity.
- Dashboards: start basic (CSV/notebook), iterate to lightweight web or hosted logs.
- Rollout strategy: shadow → beta(allowlist) → % rollout; kill switch.

## 12) Risks & Mitigations
- English documentation barrier → glossary and phrases docs; 90-day English ramp-up plan.
- Resource constraints (no GPU) → Q4 quantization, external APIs, short fine-tunes.
- Scope creep → weekly MVP first, evaluation gates before expansion.

## 13) Documentation Index
- Plan files: `Ai Engineer Development Plan.txt`, `prelearning Plan.txt` (appendix with Day 1 & 12/09 checklist).
- Agent guidance: `.github/copilot-instructions.md`.
- Communication aids: `docs/glossary.md`, `docs/phrases.md`.
- Process templates: `templates/PR_TEMPLATE.md`.

## 14) Blog & Learning Curriculum Output
- Each week’s README links to a blog post draft; include purpose/stack/quick start/demo and evaluation highlights.
- Consolidate into a structured series: "AI Engineer 기본 학습과정"—a beginner’s guide aligned with deliverables and metrics.

## 15) Acceptance Criteria (per week)
- MVP runs locally; `/health` responds; tests ≥ N pass; README quick start exists; secrets handled via `.env`.
- Metrics reported (where applicable): Retrieval@k, JSON validity, p95 latency, cost/session.
- Demo note or short Loom link placeholder.

## 16) Open Questions
- Default model mix (Ollama tags, Groq models) and fallback thresholds (timeouts)?
- Preferred evaluation dataset domain (finance/health/legal)?
- CI policy (blocking vs advisory) and minimum test count per week.

## 17) Next Actions
- Scaffold Week 1 folder with FastAPI + `/health` + `/echo`, `pytest` seeds, `.env.example`, Dockerfile, README.
- Add GitHub Actions workflow (lint/test/build) and basic metric logging.
- Prepare Week 2 evaluation harness signature (Precision/Recall/F1, Retrieval@k).

---

## Appendix A) Prelearning (3 Weeks) – Detailed Plan

Source of truth: `prelearning Plan.txt` (updated with 부록). Below summarizes goals, checkpoints, and deliverables to accelerate Week 1–2.

### Week 0‑1: Python & ML (36h)
- Goals: Python 기본(함수/리스트·딕셔너리/에러), Pandas 클린, 회귀/분류 개념, Git/SQL 인트로.
- Optional add-ons: FastAPI 기초(라우팅/Pydantic/예외), `uv` 가상환경, `.env` 사용, `pytest` 6–10개.
- Daily checkpoints: `/health`·`/echo` 스켈레톤, CSV→JSON 변환 함수 1개, Git 커밋, 테스트 1개 그린.
- Deliverables: 노트북 2–3개, 순수 함수 유틸(파일 IO/JSON/코사인), FastAPI 스켈레톤 1개.

### Week 0‑2: Data Analytics (36h)
- Goals: Excel 클린·피벗, SQL JOIN/WINDOW, Tableau 기본(또는 Streamlit 대체), Pandas→JSON 검증.
- RAG Foundations: PyPDF2→청크→코사인→top‑k, 간단 평가(toy) 포함.
- Daily checkpoints: PDF 파싱 성공, 분할 함수 테스트, Streamlit 업로드→top‑3 청크 표시.
- Deliverables: `rag_stub.ipynb`, `rag_stub_cli.py`, Streamlit MVP 1페이지.

### Week 0‑3: Integration & Review (24h)
- Goals: FastAPI(/ask)↔RAG 스텁 연동, 견고성 드릴(깨진 PDF/빈 텍스트/타임아웃), DevOps 라이트(README, `.env.example`, `.gitignore`).
- Assessments: 테스트 그린(6–10), 3개 PDF에서 관련 청크 반환, 로컬 응답 p95≤200ms.
- Deliverables: 통합 실행 가이드(README Quick Start), 간단 로그/메트릭 표.

### Day 1 Focus & 12/09 Readiness (from 부록)
- Day 1: 환경 세팅(uv/커널), Git/SQL 인트로, CSV→JSON + 테스트 1개.
- 12/09 체크: FastAPI `/health`·`/echo`, RAG 스텁 top‑k, Streamlit(선택), 테스트 6–10, 비밀키 미노출.

### English Ramp-up (30 min/day)
- Weeks 1–4: API/문서 영어(동사·요구사항 표현) + 템플릿 암기.
- Weeks 5–8: 규제/도메인 용어 200개 한‑영 카드 완성.
- Weeks 9–12: 회의 문장 30개 스크립트 암기(오픈/클로징).

Cross-links: See `docs/glossary.md`, `docs/phrases.md`, `templates/PR_TEMPLATE.md`.
