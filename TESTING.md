# PRALAYA-NET Testing & Validation Guide

## Pre-Demo Checklist

### Backend
- [ ] Python 3.8+ installed
- [ ] requirements.txt has all dependencies
- [ ] Backend starts without errors: `python -m uvicorn app:app`
- [ ] API health check works: `/api/health`
- [ ] Risk-alert endpoint works: `/api/risk-alert`
- [ ] Disaster injection works: `POST /api/trigger/inject`
- [ ] Middleware loaded (rate limiting, validation)
- [ ] Caching functional (30s TTL)
- [ ] API response time < 300ms

### Frontend
- [ ] Node.js 16+ installed
- [ ] npm dependencies installed
- [ ] `npm run build` succeeds
- [ ] Build output < 2MB
- [ ] Dashboard loads at http://localhost:5173
- [ ] Connects to backend API successfully
- [ ] CORS headers correct

### Hardware (ESP32)
- [ ] Arduino IDE installed
- [ ] ArduinoJson library installed
- [ ] Serial driver (CH340) installed
- [ ] USB connection stable
- [ ] Sketch uploads without errors
- [ ] Serial output at 115200 baud
- [ ] WiFi connects successfully
- [ ] GPIO pins configured (21, 22, 23)
- [ ] Hardware self-test passes
- [ ] Connects to backend API

---

## Backend Testing

### 1. Basic Functionality

```bash
cd backend

# Start backend
python -m uvicorn app:app --reload --port 8000

# In another terminal:
# Test health
curl http://localhost:8000/api/health

# Expected:
{
  "status": "healthy",
  "components": {
    "api": "operational",
    "ai_models": "loaded",
    "orchestration": "ready"
  }
}

# Test root
curl http://localhost:8000/

# Expected:
{
  "status": "online",
  "system": "PRALAYA-NET Backend",
  "version": "0.1.0",
  "message": "PRALAYA-NET backend is operational"
}
```

### 2. Risk Alert Endpoint

```bash
# GET risk status
curl http://localhost:8000/api/risk-alert

# Expected response:
{
  "risk_score": 0.0,
  "risk_level": "safe",
  "hardware_action": "none",
  "hardware_trigger": {
    "buzzer": false,
    "red_led": false,
    "green_led": true,
    "pulse": false,
    "intensity": 0
  },
  "timestamp": "2024-02-05T...",
  "message": "System nominal",
  "active_disasters": 0,
  "source": "live"
}
```

### 3. Disaster Injection

```bash
# Inject flood disaster
curl -X POST http://localhost:8000/api/trigger/inject \
  -H "Content-Type: application/json" \
  -d '{
    "disaster_type": "flood",
    "severity": 0.85,
    "location": {"lat": 28.6139, "lon": 77.2090}
  }'

# Expected: Disaster ID returned
# Then check risk-alert again - should show high risk

curl http://localhost:8000/api/risk-alert

# Expected: risk_score now 0.85+, red LED triggered
```

### 4. Input Validation

```bash
# Test invalid disaster type
curl -X POST http://localhost:8000/api/trigger/inject \
  -H "Content-Type: application/json" \
  -d '{
    "disaster_type": "invalid_type",
    "severity": 0.5,
    "location": {"lat": 0, "lon": 0}
  }'

# Expected: 400 error - Invalid disaster_type

# Test invalid coordinates
curl -X POST http://localhost:8000/api/trigger/inject \
  -H "Content-Type: application/json" \
  -d '{
    "disaster_type": "flood",
    "severity": 0.5,
    "location": {"lat": 200, "lon": 0}
  }'

# Expected: 400 error - Latitude out of range
```

### 5. Rate Limiting

```bash
# Spam requests (should get 429 after 100 requests)
for i in {1..110}; do
  curl http://localhost:8000/api/health -s -w "%{http_code}\n"
done

# After 100: Should see 429 Too Many Requests
# Check headers: X-RateLimit-Limit, X-RateLimit-Remaining
```

### 6. API Documentation

```bash
# Navigate to http://localhost:8000/docs
# Should show Swagger UI with all endpoints
# Click "Try it out" on /api/risk-alert
# Should get live response
```

---

## Frontend Testing

### 1. Dashboard Load

```bash
cd dashboard
npm run dev

# Visit http://localhost:5173
# Page should load without console errors
# Map should display
# Control panel should be visible
```

### 2. API Connection

Open browser DevTools (F12):

```javascript
// In Console tab:
const api = 'http://localhost:8000';
fetch(api + '/api/health')
  .then(r => r.json())
  .then(d => console.log(d));

// Expected: Health check response
```

### 3. Disaster Injection from Dashboard

- Click "Inject Disaster" in Control Panel
- Select disaster type: "flood"
- Set severity: 0.85
- Click "Inject"
- Check Network tab: POST to `/api/trigger/inject`
- Map should update with red disaster zone

### 4. Building for Production

```bash
cd dashboard

# Clean build
rm -rf dist/ node_modules/
npm install
npm run build

# Expected:
# ✓ dist/index.html
# ✓ dist/assets/*.js
# ✓ dist/assets/*.css
# Total size: < 2MB

# Test production build locally
npm run preview
# Visit http://localhost:4173
# Should work identical to dev
```

---

## Hardware Testing (ESP32)

### 1. Serial Monitor Setup

```
Arduino IDE:
Tools → Serial Monitor
Baud rate: 115200
Both NL and CR selected
```

### 2. Startup Sequence

Expected output:
```
======================================
PRALAYA-NET ESP32 Hardware Controller
======================================
Hardware initialized
Buzzer GPIO: 23
Red LED GPIO: 22
Green LED GPIO: 21

Running self-test...
Testing GREEN LED...
Testing RED LED...
Testing BUZZER...
Self-test complete!

Connecting to WiFi: YOUR_SSID
.....
WiFi connected!
IP address: 192.168.1.100
RSSI: -45 dBm

Polling backend for risk alerts...
```

### 3. Normal Operation

```
Risk Score: 0.15 | Level: safe | Action: none
>>> SAFE - Green LED ON <<<

[Green LED should be ON]
[Red LED OFF]
[Buzzer silent]
```

### 4. High Risk Alert

Inject disaster from backend or dashboard:
```
Risk Score: 0.85 | Level: high | Action: alarm
>>> ACTIVATING HIGH RISK ALERT <<<

[Red LED pulsing]
[Buzzer 2kHz pulsing sound]
[Green LED OFF]
```

### 5. WiFi Reconnection

Disconnect WiFi and reconnect:
```
WiFi disconnected!
[All LEDs blinking - error state]

WiFi connected!
IP address: 192.168.1.100
[Resume normal operation]
```

### 6. Hardware Diagnostics

```bash
# In Serial Monitor, look for:
- Successful API polling (every 10 seconds)
- Risk score updates
- GPIO state changes
- No error messages

# If errors:
- Check WiFi credentials
- Check backend URL is correct
- Check firewall settings
- Verify GPIO pins match sketch (21, 22, 23)
```

---

## Integration Testing (End-to-End)

### Scenario 1: Complete Demo Flow

```
1. Start Backend
   cd backend && python -m uvicorn app:app --port 8000

2. Start Dashboard
   cd dashboard && npm run dev

3. Upload ESP32 sketch with WiFi credentials

4. Monitor all three:
   - Terminal: Backend logs
   - Browser: http://localhost:5173
   - Serial Monitor: ESP32 output

5. Inject disaster from dashboard control panel

6. Observe:
   ✓ Backend: Processes disaster, calculates risk
   ✓ Dashboard: Red zone appears on map, risk graph updates
   ✓ ESP32: Buzzer sounds, red LED pulses
   ✓ All within < 300ms

7. Clear disaster

8. Observe:
   ✓ Backend: Risk drops to 0
   ✓ Dashboard: Zone clears, graph resets
   ✓ ESP32: Green LED ON, buzzer silent
```

### Scenario 2: Multiple Disasters

```
1. Inject flood (severity 0.7)
2. Inject earthquake (severity 0.6)

Expected: Cascading risk calculated
- Risk should be > 0.7 (higher due to cascading)
- GNN analyzes infrastructure vulnerabilities
```

### Scenario 3: Network Failure

```
1. Disconnect WiFi
2. Watch ESP32 serial: Should show WiFi error
3. LEDs should blink (error state)
4. Reconnect WiFi
5. Should resume normal polling

Expected: Graceful error handling
```

### Scenario 4: API Rate Limiting

```
1. Spam API requests (> 100/minute)
2. Should get 429 Too Many Requests
3. X-RateLimit headers should indicate limit

Expected: Rate limiting working
```

---

## Performance Benchmarking

### 1. API Response Time

```bash
# Measure risk-alert endpoint
time curl http://localhost:8000/api/risk-alert -s > /dev/null

# Expected: real < 300ms (target achieved)
```

### 2. Dashboard Build Time

```bash
cd dashboard
time npm run build

# Expected: < 10 seconds
```

### 3. Dashboard Bundle Size

```bash
cd dashboard
npm run build
du -sh dist/

# Expected: < 2MB
```

### 4. Concurrent User Load

```bash
# Install Apache Bench
ab -n 1000 -c 50 http://localhost:8000/api/health

# Expected:
# Requests per second: > 100
# Failed requests: 0
# Avg response time: < 300ms
```

---

## Security Testing

### 1. Input Validation

```bash
# SQL Injection attempt
curl -X POST http://localhost:8000/api/trigger/inject \
  -H "Content-Type: application/json" \
  -d '{"disaster_type": "'; DROP TABLE disasters;--", "severity": 0.5, "location": {"lat": 0, "lon": 0}}'

# Expected: 400 error, no database changes
```

### 2. XSS Prevention

```javascript
// In dashboard console:
fetch('http://localhost:8000/api/trigger/inject', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    disaster_type: 'flood',
    severity: 0.5,
    location: {lat: 0, lon: 0}
  })
})
.then(r => r.json())
.then(d => console.log(d));

// Expected: Sanitized response, no script execution
```

### 3. CORS Policy

```bash
# Try request from unauthorized origin
curl http://localhost:8000/api/risk-alert \
  -H "Origin: https://evil.com"

# Expected: CORS error if not in whitelist
```

### 4. Rate Limiting

```bash
# Already tested above
# Rate limiting should prevent abuse
```

---

## Pre-Demonstration Validation

Run this before demo:

```bash
#!/bin/bash

echo "=== PRALAYA-NET Pre-Demo Validation ==="

# Test backend
echo "Testing backend..."
curl -s http://localhost:8000/api/health > /dev/null && echo "✓ Backend health" || echo "✗ Backend failed"

# Test dashboard
echo "Testing dashboard build..."
cd dashboard && npm run build > /dev/null 2>&1 && echo "✓ Dashboard build" || echo "✗ Dashboard build failed"

# Test API endpoint
echo "Testing risk-alert..."
curl -s http://localhost:8000/api/risk-alert | grep "risk_score" > /dev/null && echo "✓ Risk-alert endpoint" || echo "✗ Risk-alert failed"

# Test disaster injection
echo "Testing disaster injection..."
curl -s -X POST http://localhost:8000/api/trigger/inject \
  -H "Content-Type: application/json" \
  -d '{"disaster_type":"flood","severity":0.5,"location":{"lat":0,"lon":0}}' | grep -q "disaster_id" && echo "✓ Disaster injection" || echo "✗ Disaster injection failed"

echo "=== Validation Complete ==="
```

---

## Troubleshooting Tests

### Backend Tests Fail

```bash
# Check Python installation
python --version  # Must be 3.8+

# Check port availability
lsof -i :8000

# Check dependencies
pip install -r requirements.txt --force-reinstall

# Check for import errors
python -c "import app"

# If still fails, check for syntax errors
python -m py_compile backend/*.py
```

### Frontend Tests Fail

```bash
# Check Node version
node --version  # Must be 16+

# Clean install
rm -rf node_modules package-lock.json
npm install

# Try build
npm run build

# If fails, check for missing dependencies
npm ls
```

### Hardware Tests Fail

```bash
# Check serial connection
ls -la /dev/ttyUSB*  # Linux
mode COM3           # Windows

# Check board selection
# Arduino IDE → Tools → Board → ESP32 Dev Module

# Check upload settings
# Arduino IDE → Tools → Upload Speed → 115200

# Monitor output
# Arduino IDE → Tools → Serial Monitor → 115200 baud
```

---

## Sign-Off Checklist

When all tests pass:

- [ ] Backend starts without errors
- [ ] All API endpoints respond
- [ ] Frontend builds successfully
- [ ] Dashboard displays without errors
- [ ] ESP32 uploads and runs
- [ ] End-to-end demo works
- [ ] Performance targets met
- [ ] Security validations passed
- [ ] All features documented
- [ ] Ready for hackathon!

---

Last Updated: February 2026 | Version 1.0
