# Multi-Agent MCP Server - Dockerfile for Smithery container runtime
# See: https://smithery.ai/docs/build/project-config/dockerfile

FROM python:3.11-slim

# Prevent Python from writing pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install minimal system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pre-copy dependency manifests for efficient layer caching
COPY pyproject.toml requirements.txt README.md ./

# Upgrade pip tooling and install Python dependencies
RUN python -m pip install --upgrade pip setuptools wheel \
    && if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Copy application source
COPY src ./src
COPY mcp.json ./mcp.json

# Install the package (editable to keep paths simple)
RUN pip install -e .

# Ensure src is importable for module-based entry
ENV PYTHONPATH=/app/src

# Default command for local runs (Smithery overrides via startCommand)
CMD ["python", "-u", "-m", "multiagent_mcp_server.server"]
