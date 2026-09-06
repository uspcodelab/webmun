# ------------------
# Build stage
# ------------------

FROM python:3.11-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml uv.lock .

# ------------------
# Development env
# ------------------
FROM base AS development

# By copying only the uv lock files, we dont recheck with uv sync everytime a line of python is changed
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# notice how we dont copy source code here: it is redundant, since we have bind mount

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]

# ------------------
# Prod stage
# ------------------
FROM base AS prod-builder

ENV UV_NO_DEV=1

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# here we do copy, since we wont use bind mount
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# ------------------
# Prod stage
# ------------------

FROM python:3.11-slim AS production

WORKDIR /app

RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy .venv with project dependencies and source code
COPY --from=prod-builder /app/.venv /app/.venv
COPY --from=prod-builder --chown=appuser:appuser /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER appuser
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
