#!/bin/bash
# Production start script for Render - Python 3.12 optimized
set -e

echo "🚀 Starting PRALAYA-NET Backend in Production Mode (Python 3.12)"

# Ensure we are in the backend directory
cd "$(dirname "$0")"

echo "📦 Python version: $(python --version)"
echo "📦 pip version: $(pip --version)"

# Upgrade pip, setuptools, and wheel if needed
echo "🔧 Ensuring build tools are up-to-date..."
pip install --upgrade pip setuptools wheel --quiet

# Check if requirements.txt exists and install dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies from requirements.txt..."
    pip install --no-cache-dir -r requirements.txt
fi

# Start uvicorn for production
echo "🌐 Starting server..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info --workers 1

