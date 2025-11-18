# AGENT CONTEXT — quick resume

Last action
- Last merged PR: #2 (plan/integrate-linuxmint-wordpress) — integrated prelearning into plan; updated Linux Mint; added WordPress generator
- Last commit: see `git log -n 5` for recent commits

Key anchors
- Plan: `docs/Integrated_plan.md`
- Week1 skeleton: `Grok-AI-Engineer-5Months/01_Week1_FastAPI_Chatbot/src/main.py`
- WordPress course templates: `docs/wordpress_course.md`, `docs/wordpress_course/week-*.md`
- LinkedIn drafts: `docs/linkedin_posts/`
- Auto-generator: `scripts/generate_wordpress_chapters.py`
- Agent guidance: `.github/copilot-instructions.md`

Open tasks
- `week0/day1`: add lecture notes (docs/lecture_week0_day1.md)
- `week0/day1`: implement `src/utils/csv_to_json.py` + tests in `tests/`
- `week1`: expand FastAPI (/health /echo), add tests, Dockerfile run check
- `docs`: WordPress publish GitHub Action (optional)

Environment & quick commands (Linux Mint)
- Setup:
  ```bash
  python3 -m venv .venv && source .venv/bin/activate
  pip install --upgrade pip pip-tools || true
  pip-compile requirements.in || true
  pip install -r requirements.txt
  ```
- Run dev server:
  ```bash
  python -m uvicorn src.main:app --reload --port 8000
  ```
- Regenerate WP chapters:
  ```bash
  python3 scripts/generate_wordpress_chapters.py
  ```
- Tests:
  ```bash
  pytest -q
  ```

Resume prompt template (recommended)
- English: "Resume from AGENT_CONTEXT.md. Task: <task-id>. Branch: <branch>. Run tests: pytest -q. If files missing scaffold minimal artifacts. Commit message: feat(<task>): short description." 
- Korean: "AGENT_CONTEXT.md 기준으로 이어가 주세요. 작업: <작업코드>. 브랜치: <브랜치명>. 테스트: pytest -q. 파일 없다면 스캐폴드 및 테스트 생성." 

How to update AGENT_CONTEXT.md
- After completing a task: add a single bullet: `DONE: <task> — <short sha>`
- If blocked: add `BLOCKED: <reason>` and link to issue/PR

PR checklist suggestion
- [ ] AGENT_CONTEXT.md updated
- [ ] Quick commands included in PR description
- [ ] Next tasks prioritized

Example resume command the user can say next time:
- "Resume: AGENT_CONTEXT. Branch=week0/day1-csv-util. Task=implement csv util + tests. Run tests and push PR."
