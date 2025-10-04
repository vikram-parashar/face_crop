FROM ghcr.io/astral-sh/uv:debian-slim

RUN apt-get update && \
    apt-get install -y build-essential cmake

WORKDIR /app
COPY main.py /app
COPY pyproject.toml /app
COPY uv.lock /app 

ENV PATH="/app/.venv/bin:$PATH"
RUN uv sync --no-dev

ENTRYPOINT ["python", "main.py"]
