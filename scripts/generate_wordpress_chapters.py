#!/usr/bin/env python3
"""
Generate WordPress chapter markdown files from the main plan file.
Reads `Ai Engineer Development Plan.txt`, extracts Week titles, and writes `docs/wordpress_course/week-<n>-chapter.md` files.
"""
import re
from pathlib import Path

PLAN_FILE = Path(__file__).parents[1] / 'Ai Engineer Development Plan.txt'
OUT_DIR = Path(__file__).parents[1] / 'docs' / 'wordpress_course'
OUT_DIR.mkdir(parents=True, exist_ok=True)

def parse_weeks(text):
    # find lines like: | **Week 1** | **첫 AI 앱 배포** | ...
    pattern = re.compile(r"\| \*\*(Week\s+[0-9.]+)\*\* \| \*\*(.*?)\*\*")
    weeks = []
    for m in pattern.finditer(text):
        week_id = m.group(1).strip()
        title = m.group(2).strip()
        weeks.append((week_id, title))
    return weeks

def render_chapter(week_id, title):
    n = week_id.split()[1]
    return f"""---
title: "{title}"
week: {n}
---

# {title}

Summary: Write a 1–2 sentence summary of the week objectives and deliverables.

## Objectives
- Objective 1
- Objective 2

## Commands & quick start
```bash
# Setup venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
``` 

## Code & notebooks
- `notebooks/` - link sample notebooks
- `src/` - link week code

## Demo (Loom)
- Loom placeholder link

## LinkedIn suggestions
- #{n}-1: Short post title
- # {n}-2: Short post title
"""

def main():
    text = PLAN_FILE.read_text(encoding='utf-8')
    weeks = parse_weeks(text)
    # Prepend Week 0 candidate using prelearning header if present
    if 'Week 0' not in [w[0] for w in weeks]:
        weeks.insert(0, ('Week 0', 'Prelearning — Python & ML'))

    index_lines = ["# WordPress Course - Chapters\n\n"]
    for week_id, title in weeks:
        week_num = week_id.split()[1]
        fname = OUT_DIR / f"week-{week_num}-chapter.md"
        fname.write_text(render_chapter(week_id, title), encoding='utf-8')
        index_lines.append(f"- [Week {week_num}: {title}](week-{week_num}-chapter.md)\n")

    (OUT_DIR / 'index.md').write_text('\n'.join(index_lines), encoding='utf-8')
    print(f"Generated {len(weeks)} chapter files in {OUT_DIR}")

if __name__ == '__main__':
    main()
