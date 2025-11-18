# Integrated AI Engineer Plan (v4.1 candidate)

This file merges `prelearning Plan.txt` with `Ai Engineer Development Plan.txt` so the course contains a complete, chronological set of steps. Prelearning becomes Weeks 0–2 to ensure learners start Week 1 with a solid foundation.

Key updates in this candidate:
- Prelearning block now explicitly Weeks 0–2 (3 weeks): Python/ML basics, Data Analytics, Integration & SME simulation.
-- Development laptop = Linux Mint for Weeks 1–7. (This is the preferred local Linux development environment for the plan.)
- LinkedIn / WordPress pipeline: daily/weekly posts and free-course chapters will be used as portfolio and course content.
- Minimal venv & `requirements.in` compile sequence documented for Linux Mint.

## Week 0–2 (Prelearning summary)
- Week 0-1: Python & ML (Le Wagon style), daily demos & small notebooks, Git + `pytest` seed tests
- Week 0-2: Excel/SQL/Tableau or Streamlit, Pandas → JSON, RAG foundations (PyPDF2 → chunk → cosine → top-k)
- Week 0-3: Integration + robustness drills, small RAG stubs and Streamlit upload demo

## OS & Environment
- Primary developer machine: **Linux Mint** (Weeks 1–7)
- Quick setup:
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y python3 python3-venv python3-pip build-essential git docker.io
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

## LinkedIn → WordPress pipeline
- Daily LinkedIn micro-posts during prelearning and early weeks become weekly chapter pages on WordPress
- `docs/linkedin_posts/` stores markdown drafts; each Saturday compile a chapter to `docs/wordpress_course/` for publishing

## Next steps
- Review this integrated candidate and confirm merging into `Ai Engineer Development Plan.txt`.
- If confirmed, the next PR will replace the top portion of the plan with this consolidated content and bump the version.
