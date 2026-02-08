# PRALAYA-NET Render Deployment Guide

## Deployment Configuration - Python 3.12

This guide provides the fixed configuration for deploying PRALAYA-NET on Render without the `setuptools.build_meta` import error.

## Quick Start

### Option 1: Deploy Using Render Dashboard

1. **Connect Repository**: Connect your GitHub repository to Render
2. **Create Web Service**: Select the repository and configure:
   - **Environment**: Python
   - **Python Version**: `3.12`
   - **Build Command**:
     ```bash
     pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
3. **Environment Variables**: Add these in the Render dashboard:
   ```
   NASA_API_KEY=<your_key_here>
   DATA_GOV_KEY=<your_key_here>
   OPENWEATHER_API_KEY=<your_key_here>
   PORT=8000
   DEMO_MODE=true
   ```

### Option 2: Deploy Using render.yaml

Render will automatically detect `render.yaml` in the root directory and use it for deployment.

## Files Configuration

### backend/render.yaml (Recommended)
```yaml
services:
  - type: web
    name: PRALAYA-NET
    env: python
    pythonVersion: "3.12"
    buildCommand: |
      pip install --upgrade pip setuptools wheel
      pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: NASA_API_KEY
        value: <your_key_here>
      - key: DATA_GOV_KEY
        value: <your_key_here>
      - key: OPENWEATHER_API_KEY
        value: <your_key_here>
      - key: PORT
        value: 8000
      - key: DEMO_MODE
        value: "true"
    plan: starter
    region: oregon
    healthCheckPath: /health
    autoDeploy: true
```

### backend/pyproject.toml
```toml
[build-system]
requires = ["setuptools>=69.0.0", "wheel"]
build-backend = "setuptools.build_meta"
```

### backend/requirements.txt
```
# Build System - CRITICAL: Must be at the top and upgraded first
setuptools>=69.0.0
wheel>=0.42.0
pip>=24.0

# Core Framework
fastapi>=0.109.0
uvicorn[standard]>=0.27.0

# Data Validation
pydantic>=2.5.3

# HTTP & Async
httpx>=0.26.0
aiofiles>=23.2.1
python-multipart>=0.0.9

# Web & Networking
websockets>=12.0
requests>=2.31.0
python-dotenv>=1.0.1

# Data Science & ML
numpy>=1.26.0
networkx>=3.3

# Security
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
```

## Why Python 3.12?

Python 3.12 offers:
- Better performance (10-25% faster than 3.11)
- Improved error messages
- Better package compatibility
- No changes required to existing code
- Most packages have stable wheels available

## Why This Fixes the Error

The `BackendUnavailable: Cannot import 'setuptools.build_meta'` error occurred because:

1. **Build tools upgrade order**: The `pip install --upgrade pip setuptools wheel` command runs FIRST before installing any packages
2. **PEP 517/518 compliance**: The `[build-system]` section now uses compatible versions
3. **Minimal dependencies**: `setuptools>=69.0.0` is sufficient and widely available
4. **No problematic packages**: torch, opencv-python are not included (these often fail on Python 3.13)

## Docker Deployment

If using Docker, the Dockerfile is configured with:

```dockerfile
FROM python:3.12-slim

# Upgrade build tools FIRST
RUN pip install --upgrade pip setuptools wheel

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Local Testing

```bash
# Verify Python version
python --version  # Should be 3.12.x

# Upgrade build tools
pip install --upgrade pip setuptools wheel

# Test installation
cd backend
pip install -r requirements.txt

# Verify installation
python -c "import setuptools; print(f'setuptools: {setuptools.__version__}')"
python -c "import uvicorn; print(f'uvicorn: {uvicorn.__version__}')"
python -c "import fastapi; print(f'fastapi: {fastapi.__version__}')"

# Run the app
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Health Check

After deployment, verify with:
```bash
curl https://<your-service>.onrender.com/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00.000000",
  "service": "PRALAYA-NET Backend"
}
```

## Troubleshooting

### Still getting setuptools error?
Ensure the build command includes the upgrade:
```bash
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
```

### Package compatibility issues?
Python 3.12 has excellent package compatibility. If you encounter issues:
1. Check if the package supports Python 3.12
2. Try updating to the latest version
3. Contact package maintainers for Python 3.12 support

### Docker build fails?
Ensure you're using Python 3.12 base image:
```dockerfile
FROM python:3.12-slim
```

## Environment Variables

| Variable | Value | Required |
|----------|-------|----------|
| NASA_API_KEY | Your NASA API key | No (demo mode works without) |
| DATA_GOV_KEY | Your Data.gov API key | No (demo mode works without) |
| OPENWEATHER_API_KEY | Your OpenWeather API key | No (demo mode works without) |
| PORT | 8000 | Yes (Render sets this) |
| DEMO_MODE | true | Recommended |

## Rollback Plan

If issues occur, Render provides automatic rollback. Manually:
1. Change `pythonVersion` to `"3.11"` in render.yaml
2. Update `requires-python` in pyproject.toml to `">=3.11"`
3. Redeploy

## Support

- Check Render build logs for specific errors
- Verify all environment variables are set
- Ensure repository is connected correctly

