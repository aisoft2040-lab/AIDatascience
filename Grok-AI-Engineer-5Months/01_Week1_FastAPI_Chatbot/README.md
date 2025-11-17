# Week 1 – FastAPI Chatbot Skeleton

Purpose: Minimal FastAPI app with health and echo endpoints, ready for fallback orchestration.

## Quick Start (cmd.exe)
```
uv pip compile -q -o requirements.txt requirements.in
uv pip install -r requirements.txt
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Test:
```
pytest -q
```

Health:
- GET http://localhost:8000/health → {"status":"ok","version":"<env>"}

Echo:
- POST http://localhost:8000/echo {"message":"hello"}

Docker:
```
docker build -t week1-fastapi .
docker run -p 8000:8000 -e APP_VERSION=container week1-fastapi
```

Env:
- Copy `.env.example` → `.env` and export as needed. APP_VERSION defaults to `dev` when unset.
