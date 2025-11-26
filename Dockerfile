# file: Dockerfile

# ---------------------------------------------------------
# STAGE 1 — Builder
# ---------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y build-essential gcc && \
    apt-get clean

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# ---------------------------------------------------------
# STAGE 2 — Final
# ---------------------------------------------------------
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local
COPY ./src ./src
COPY ./alembic.ini .

ENV PYTHONPATH=/app

EXPOSE 8000

# Railway usa la variable PORT automáticamente
ENV PORT=8000

# Gunicorn + Uvicorn Worker (best practice)
CMD gunicorn src.app.main:app \
    --pythonpath /app \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:$PORT \
    --timeout 120 \
    --workers 1


# end file: Dockerfile
