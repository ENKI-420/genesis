# GENESIS Sovereign Platform
# Multi-stage build for optimized container

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml setup.py ./
COPY src/ ./src/

# Build wheel
RUN pip install --no-cache-dir build && \
    python -m build --wheel

# Runtime stage
FROM python:3.11-slim as runtime

WORKDIR /app

# Create non-root user
RUN groupadd -r genesis && useradd -r -g genesis genesis

# Copy built wheel from builder
COPY --from=builder /app/dist/*.whl /tmp/

# Install the package
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm /tmp/*.whl

# Copy additional files
COPY config/ ./config/
COPY examples/ ./examples/

# Switch to non-root user
USER genesis

# Default configuration
ENV GENESIS_CONFIG_PATH=/app/config/default.yaml
ENV GENESIS_LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD genesis status || exit 1

# Default command
ENTRYPOINT ["genesis"]
CMD ["--help"]

# Labels
LABEL org.opencontainers.image.title="GENESIS Sovereign Platform"
LABEL org.opencontainers.image.description="Quantum-inspired autopoietic computational framework"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="GENESIS Project"
LABEL org.opencontainers.image.licenses="GENESIS-1.0"
