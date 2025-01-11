FROM python:3.12-slim-bookworm

WORKDIR /app

RUN python3 -m venv .venv && \
    .venv/bin/python -m pip install --upgrade pip && \
    .venv/bin/python -m pip install uv && \
    .venv/bin/python -m pip install pytest torch

# Copy requirements and install dependencies
COPY uv.lock .
COPY pyproject.toml .
RUN .venv/bin/python -m uv sync

# Copy source code
COPY src src

# Warm image by running tests
COPY tests tests
ENV PYTHONPATH=.
RUN .venv/bin/python -m pytest

COPY README.md .
CMD [".venv/bin/python", "-m", "uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
