# Stage 1: Build stage - create virtual environment
FROM python:3.14-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files
COPY pyproject.toml .
COPY uv.lock .

# Create virtual environment and install dependencies
RUN uv sync --frozen --no-dev

# Stage 2: Runtime stage - slim image with only .venv and app
FROM python:3.14-alpine

WORKDIR /app

# Prevents Python from writing .pyc files to disk - saves space
ENV PYTHONDONTWRITEBYTECODE=1 
# Ensures that Python output is sent straight to terminal (e.g. for logging) and not buffered
ENV PYTHONUNBUFFERED=1

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY pyproject.toml .
COPY main.py .
COPY src/ ./src

# Use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# expose 4600 port
EXPOSE 4600

CMD ["python", "main.py"]

