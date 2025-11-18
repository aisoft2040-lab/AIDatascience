# WordPress Free Course: AI Engineer Journey

Purpose: use daily LinkedIn microposts as public learning material; compile weekly chapters for free course content on your WordPress site. Keep code and notebooks in GitHub and link to them from WordPress.

How it works
- `docs/linkedin_posts/` — store daily micro-post drafts and assets
- Saturday: compile the daily posts of the week into `docs/wordpress_course/week-N-chapter.md`
- Publish to WordPress under category `AI Engineer Journey / 5-Month Challenge`

Chapter template
- Title
- Week objective
- Short summary (100—200 words)
- Key commands & code snippets (copyable)
- Links to GitHub code + notebooks
- Loom demo placeholder
- Suggested LinkedIn micro-posts for the next week

Week 0 example (Week 0: Prelearning — Python & ML)
- Title: Week 0 — Python & ML Foundations
- Objective: cover Python basics, Pandas and a simple ML pipeline
- Key commands:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  pytest -q
  python -m uvicorn src.main:app --reload --port 8000
  ```
- Code artifacts: `notebooks/python-ml-basics.ipynb`, `src/utils/csv_to_json.py`
- WordPress SEO tags: `prelearning`, `python`, `pandas`, `rAG`, `data-science`

Licensing & links
- Use CC BY-SA for course content so readers can reuse code and notes
- Link to GitHub repo for exercises and unit tests
