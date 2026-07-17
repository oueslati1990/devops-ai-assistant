# Stage 1: install dependencies
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Stage 2: minimal runtime image
FROM python:3.14-slim
WORKDIR /app

# Copy the virtualenv from builder instead of individual packages
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY app/ ./app/

ENV PATH=/app/.venv/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]