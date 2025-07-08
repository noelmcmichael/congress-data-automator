# Multi-stage Dockerfile for Congressional Data API Service

# Stage 1: Build dependencies
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DEPS="build-essential curl"
ARG POETRY_VERSION=1.6.1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends $BUILD_DEPS && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==$POETRY_VERSION

# Set Poetry configuration
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --only=main --no-root && \
    rm -rf $POETRY_CACHE_DIR

# Stage 2: Production image
FROM python:3.11-slim as production

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH" \
    ENVIRONMENT=production

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r apiuser && \
    useradd -r -g apiuser -d /app -s /bin/bash apiuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=apiuser:apiuser . .

# Switch to non-root user
USER apiuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8003/health')"

# Expose port
EXPOSE 8003

# Default command
CMD ["python", "main.py", "api"]