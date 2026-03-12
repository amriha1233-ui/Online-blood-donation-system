# Multi-stage Dockerfile for Django OBDMS Project
# Optimized for production deployment

# Stage 1: Builder - Install dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime - Production image
FROM python:3.11-slim

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 django

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/django/.local

# Copy application code
COPY --chown=django:django . .

# Create necessary directories and make entrypoint executable
RUN mkdir -p /app/logs /app/media /app/staticfiles && \
    chown -R django:django /app && \
    chmod +x /app/entrypoint.sh

# Set environment variables
ENV PATH=/home/django/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Use non-root user
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run entrypoint script (handles migrations, collectstatic, and gunicorn)
ENTRYPOINT ["/app/entrypoint.sh"]
