# Deployment Fix TODO List

## ✅ Tasks Completed

- [x] Updated `backend/pyproject.toml` to use Python 3.12 with setuptools>=69.0.0
- [x] Updated `backend/requirements.txt` with build tools at top and Python 3.12 compatible packages
- [x] Updated `backend/render.yaml` with correct Python 3.12 configuration and API keys
- [x] Updated `backend/Dockerfile` for Python 3.12 with proper build tool upgrade
- [x] Updated `backend/render-start.sh` for Python 3.12
- [x] Updated `render.yaml` (root level) to point to backend directory
- [x] Updated root `Dockerfile` for full deployment
- [x] Updated `DEPLOYMENT.md` with complete deployment guide

## Ready to Deploy

### Option 1: Render Dashboard
1. Connect repository to Render
2. Select `backend/` as the root directory for the service
3. Use Python 3.12
4. Build Command: `pip install --upgrade pip setuptools wheel && pip install -r requirements.txt`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (NASA_API_KEY, DATA_GOV_KEY, OPENWEATHER_API_KEY, PORT=8000, DEMO_MODE=true)

### Option 2: Automatic with render.yaml
Render will auto-detect `backend/render.yaml` and deploy automatically

## Key Changes Summary

| File | Change |
|------|--------|
| `backend/pyproject.toml` | Python 3.12, setuptools>=69.0.0 |
| `backend/requirements.txt` | Build tools at top, Python 3.12 compatible |
| `backend/render.yaml` | Python 3.12, build/start commands, API keys |
| `backend/Dockerfile` | Python 3.12-slim, proper build tool order |
| `render.yaml` | Updated to point to backend/ |
| `DEPLOYMENT.md` | Complete deployment guide |

## Verification Commands

```bash
# Test locally
cd backend
python --version  # Should show 3.12.x
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
# Visit http://localhost:8000/health
```

