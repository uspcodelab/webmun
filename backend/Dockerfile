FROM python:3.11-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY . .

ENV UV_NO_DEV=1

RUN uv sync --locked

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "--port", "8000"]



