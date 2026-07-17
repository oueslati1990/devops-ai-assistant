# Stage 1: install dependencies
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Stage 2: minimal runtime image
FROM python:3.14-slim
WORKDIR /app

# Copy the virtualenv from builder — uv itself is not needed at runtime
COPY --from=builder /app/.venv /app/.venv

COPY . .

ENV PATH=/app/.venv/bin:$PATH
ENV PYTHONUNBUFFERED=1

RUN useradd -m appuser && chown -R appuser /app
USER appuser

CMD ["python", "server.py"]
