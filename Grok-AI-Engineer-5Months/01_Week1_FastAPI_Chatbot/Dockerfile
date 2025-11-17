# Minimal Python slim + uv install
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY requirements.in /app/
RUN uv pip compile -q -o requirements.txt requirements.in && \
    uv pip install -r requirements.txt

COPY . /app

ENV APP_VERSION=container
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
