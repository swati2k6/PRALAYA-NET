# PRALAYA-NET Deployment Guide

**Production Deployment to Render + Vercel**

## Pre-Deployment Checklist

- [ ] All environment variables configured
- [ ] API keys from data.gov stored securely
- [ ] .env file never committed (use .env.example)
- [ ] npm run build succeeds without errors
- [ ] Backend tests pass
- [ ] No console errors in development
- [ ] CORS origins updated for production URLs
- [ ] Rate limiting configured appropriately
- [ ] API response times < 300ms
- [ ] ESP32 hardware tested locally

## Backend Deployment (Render.com)

### Step 1: Prepare GitHub Repository

```bash
# Ensure code is committed
git status
git add .
git commit -m "Production-ready deployment"

# Verify backend structure
ls -la backend/
# Should contain: app.py, config.py, middleware.py, requirements.txt
```

### Step 2: Create Render Service

1. Go to **https://render.com** and sign in
2. Click **"New +"** → **"Web Service"**
3. **Connect GitHub repository**
   - Select your PRALAYA-NET repository
   - Grant permissions if needed

4. **Configure Service**
   ```
   Name: pralaya-net-backend
   Environment: Python 3.11
   Region: Select closest to users
   Branch: main
   ```

5. **Build Settings**
   ```
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

6. **Environment Variables** (Add in Render dashboard)
   ```
   DATA_GOV_KEY=your_api_key_from_data.gov
   BACKEND_PORT=10000
   CORS_ORIGINS=https://your-vercel-frontend.vercel.app
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

7. **Click "Create Web Service"**
   - Render auto-deploys
   - Monitor deployment logs
   - Should complete in 3-5 minutes

### Step 3: Verify Backend Deployment

```bash
# Test health endpoint
curl https://pralaya-net-backend.onrender.com/api/health

# Expected response:
# {"status":"healthy","components":{"api":"operational"...}}

# Test API docs
curl https://pralaya-net-backend.onrender.com/docs

# Test risk-alert endpoint
curl https://pralaya-net-backend.onrender.com/api/risk-alert
```

### Step 4: Configure Auto-Deployment

In Render dashboard:
- Auto-deploys enabled by default
- Deploys on every git push to main
- Review logs under "Logs" tab
- Check deployment history under "Events"

---

## Frontend Deployment (Vercel.com)

### Step 1: Prepare Dashboard Build

```bash
cd dashboard

# Test production build locally
npm run build

# Expected: dist/ folder created with no errors
# Size should be < 1MB

ls -la dist/
# Verify: index.html, assets/ folder present
```

### Step 2: Create Vercel Project

1. Go to **https://vercel.com** and sign in
2. Click **"Add New +"** → **"Project"**
3. **Import GitHub repository**
   - Select PRALAYA-NET repository
   - Click "Import"

4. **Configure Project**
   ```
   Project Name: pralaya-net
   Framework Preset: Vite
   ```

5. **Build Settings**
   ```
   Build Command: npm run build
   Output Directory: dashboard/dist
   Root Directory: dashboard/
   ```

6. **Environment Variables** (Add before deploying)
   ```
   VITE_API_URL=https://pralaya-net-backend.onrender.com
   VITE_WS_URL=wss://pralaya-net-backend.onrender.com
   ```

7. **Deploy**
   - Click "Deploy"
   - Vercel builds and deploys
   - Shows deployment URL when complete

### Step 3: Verify Frontend Deployment

```bash
# Visit your Vercel URL: https://pralaya-net.vercel.app

# In browser DevTools (F12):
# - Check Network tab: All requests to backend should succeed
# - Check Console: No CORS errors
# - Check Dashboard: Should load and display empty map
```

### Step 4: Test Full Integration

```bash
# From Vercel frontend
1. Open https://pralaya-net.vercel.app
2. Open DevTools (F12)
3. Go to Network tab
4. Inject disaster via control panel or API:

curl -X POST https://pralaya-net-backend.onrender.com/api/trigger/inject \
  -H "Content-Type: application/json" \
  -d '{
    "disaster_type": "flood",
    "severity": 0.85,
    "location": {"lat": 28.6139, "lon": 77.2090}
  }'

5. Watch frontend for:
   - Red disaster zone appears on map
   - Risk graph updates
   - Alerts displayed
```

---

## ESP32 Hardware Deployment

### Prerequisites

- ESP32 DevKit V1
- Arduino IDE installed
- ArduinoJson library installed
- Hardware wired (GPIO 21, 22, 23)
- WiFi network available
- Backend running (or Render URL available)

### Step 1: Install Dependencies

```bash
# In Arduino IDE:
1. Tools → Manage Libraries
2. Search "ArduinoJson"
3. Install by Benoit Blanchon (latest version)
```

### Step 2: Configure Sketch

Open: `esp32_control/pralaya_esp32.ino`

Edit these lines:
```cpp
// Line ~24: WiFi credentials
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Line ~25: Backend URL (for production)
const char* BACKEND_URL = "https://pralaya-net-backend.onrender.com";
```

### Step 3: Upload to ESP32

1. Connect ESP32 via USB cable
2. Arduino IDE: **Tools → Board → ESP32 Dev Module**
3. **Tools → Port → Select serial port**
4. **Sketch → Upload** (or Ctrl+U)
5. Monitor output: **Tools → Serial Monitor**
   - Baud rate: **115200**
   - Expected output:
     ```
     ======================================
     PRALAYA-NET ESP32 Hardware Controller
     ======================================
     Hardware initialized
     ...
     WiFi connected
     IP: 192.168.x.x
     ```

### Step 4: Verify Hardware

Open Serial Monitor (115200 baud):

```
Expected self-test output:
Running self-test...
Testing GREEN LED...
Testing RED LED...
Testing BUZZER...
Self-test complete!

Connecting to WiFi...
WiFi connected!
IP: 192.168.1.100
RSSI: -45 dBm

Risk Score: 0.15 | Level: safe | Action: none
>>> SAFE - Green LED ON <<<
```

### Step 5: Test Hardware Integration

```bash
# In one terminal, trigger alert from backend
curl -X POST https://pralaya-net-backend.onrender.com/api/risk-alert/trigger-test

# Watch ESP32 Serial Monitor for:
Risk Score: 0.85 | Level: high | Action: alarm
>>> ACTIVATING HIGH RISK ALERT <<<

# Observe:
- Red LED starts pulsing
- Buzzer sounds (pulsed tone)
```

---

## Monitoring & Maintenance

### Backend Monitoring (Render)

1. **View Logs**
   - Render Dashboard → pralaya-net-backend → Logs
   - Check for errors: `ERROR`, `exception`, `traceback`
   - Monitor rate limit metrics

2. **Performance**
   - Watch response times
   - Check CPU/Memory usage
   - Monitor API endpoints under load

3. **Auto-Restart**
   - Render auto-restarts failed services
   - Check "Events" tab for restarts

### Frontend Monitoring (Vercel)

1. **View Analytics**
   - Vercel Dashboard → Analytics
   - Track Core Web Vitals
   - Monitor deployment status

2. **Performance**
   - Check build times
   - Monitor bundle size
   - Review first-load JS

3. **Error Tracking**
   - Check deployment logs
   - Review build warnings

### Set Up Alerts

**Render Alerts:**
- Dashboard → Settings → Notifications
- Enable email for failed deployments

**Vercel Alerts:**
- Project Settings → Notifications
- Enable email for deployment failures

---

## Troubleshooting Deployment

### Backend Won't Deploy (Render)

**Issue**: Build fails
```bash
# Check logs in Render
# Common issues:
1. Missing requirements.txt
2. Python version mismatch
3. Environment variable not set
4. Import errors

# Solution: Fix locally, commit, push
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --port 8000
# If works locally, push to GitHub
```

**Issue**: Health check fails
```bash
# In Render logs, look for:
# CONNECTION_REFUSED or 500 errors

# Solutions:
1. Check if app starts: See Render logs
2. Verify environment variables set
3. Check CORS_ORIGINS includes Vercel URL
4. Test endpoint: curl https://your-url/api/health
```

### Frontend Won't Deploy (Vercel)

**Issue**: Build fails
```bash
# Run locally first:
cd dashboard
npm ci  # Clean install
npm run build

# If build fails locally, fix before deploying
# If builds locally but fails on Vercel:
1. Check Node version in Vercel settings
2. Clear build cache: Vercel Dashboard → Settings → Git
3. Redeploy
```

**Issue**: Can't reach backend
```bash
# In browser console (F12):
CORS error? Origin not allowed

# Solution:
1. Verify CORS_ORIGINS in backend includes Vercel URL
2. Redeploy backend
3. Wait 5 minutes for changes to propagate
4. Hard refresh frontend (Ctrl+Shift+R)
```

### ESP32 Won't Connect

**Issue**: WiFi connection fails
```
Connecting to WiFi...
WiFi connection timeout!

Solutions:
1. Verify SSID and password match exactly
2. Check if 2.4GHz WiFi (ESP32 doesn't support 5GHz)
3. Move ESP32 closer to router
4. Restart router
5. Check if WiFi has MAC filtering enabled
```

**Issue**: Can't reach backend
```
HTTP Error or timeout

Solutions:
1. Verify backend URL is correct
2. Check ESP32 has internet access: ping 8.8.8.8
3. Check firewall isn't blocking
4. Test with: curl from ESP32 serial or computer
5. Check backend CORS allows ESP32 IP
```

---

## Production Checklist

Before launching to public:

### Security
- [ ] .env file never committed (use .env.example)
- [ ] API keys rotated and stored securely
- [ ] CORS origins restricted to your domains
- [ ] Rate limiting configured (100 req/min default)
- [ ] HTTPS enforced (Render + Vercel auto-enforce)
- [ ] Input validation enabled
- [ ] Error messages don't leak sensitive info

### Performance
- [ ] npm run build < 5 seconds
- [ ] npm run build output < 2MB
- [ ] API response times < 300ms (check Render metrics)
- [ ] Caching headers configured (30s TTL)
- [ ] Gzip compression enabled

### Reliability
- [ ] Backend auto-restart configured
- [ ] Frontend auto-deploy enabled
- [ ] Error monitoring set up
- [ ] Backup strategy documented
- [ ] Rollback procedure documented
- [ ] Uptime monitoring enabled

### Testing
- [ ] Full stack tested: Frontend → Backend → Database
- [ ] Error scenarios tested (API down, network error, etc.)
- [ ] Hardware (ESP32) tested with production API
- [ ] Load testing (100+ concurrent users)
- [ ] Security testing (SQL injection, XSS, etc.)

---

## Rollback Procedure

### If Backend Deployment Fails

```bash
# Render auto-maintains previous version
# In Render Dashboard:
1. Go to pralaya-net-backend
2. Click "Deployments"
3. Find previous successful deployment
4. Click "Redeploy"
# Service rolls back instantly
```

### If Frontend Deployment Fails

```bash
# Vercel auto-maintains previous version
# In Vercel Dashboard:
1. Go to project
2. Click "Deployments"
3. Find previous successful deployment
4. Click "..."  menu
5. Select "Promote to Production"
# Frontend rolls back instantly
```

### Manual Rollback via Git

```bash
# If something seriously wrong:
git log --oneline
git revert <commit-hash>
git push origin main

# Render and Vercel auto-redeploy new commit
```

---

## Cost Estimation

### Render
- Free tier: Limited hours, auto-pauses
- Starter: $7/month per service
- Standard: $25/month per service

### Vercel
- Free tier: Limited bandwidth
- Pro: $20/month

### NASA/Data.gov APIs
- Free tier: Unlimited requests (rate-limited)
- Recommended for hackathon/demo

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Arduino Docs**: https://www.arduino.cc/reference/en

---

Last Updated: February 2026 | Version 1.0
