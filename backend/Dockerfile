# PRALAYA-NET Production Dockerfile - Python 3.12
# Fixed for setuptools.build_meta compatibility

# Use Python 3.12 with slim image for faster builds
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ⚠️ CRITICAL: Upgrade pip, setuptools, and wheel FIRST
# This fixes the "BackendUnavailable: Cannot import 'setuptools.build_meta'" error
RUN pip install --upgrade pip setuptools wheel

# Copy requirements first (for better caching)
COPY pyproject.toml .
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY app.py .
COPY config.py .
COPY middleware.py .
COPY websocket_manager.py .

# Create data directories
RUN mkdir -p data/disaster_history data/predictions

# Copy api, services, orchestration directories
COPY api/ ./api/
COPY services/ ./services/
COPY orchestration/ ./orchestration/
COPY drone/ ./drone/
COPY ai/ ./ai/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

