# PRALAYA-NET Quick Reference

## 🚀 Get Started (5 Minutes)

```bash
# Terminal 1: Backend
cd backend && python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
python -m uvicorn app:app --reload

# Terminal 2: Dashboard
cd dashboard && npm install && npm run dev

# Terminal 3: Test
curl -X POST http://localhost:8000/api/risk-alert
```

**URLs**:
- 🖥️ Dashboard: http://localhost:5173
- 🔌 Backend: http://localhost:8000
- 📖 API Docs: http://localhost:8000/docs

---

## 🔐 Environment Setup

```bash
# Create .env file
cp .env.example .env

# Edit with your API key from https://api.data.gov/
DATA_GOV_KEY=your_key_here
```

---

## 🧪 Test Disaster Injection

```bash
curl -X POST http://localhost:8000/api/trigger/inject \
  -H "Content-Type: application/json" \
  -d '{
    "disaster_type": "flood",
    "severity": 0.85,
    "location": {"lat": 28.6139, "lon": 77.2090}
  }'
```

**Expected**: Dashboard shows red zone, ESP32 buzzer activates

---

## 📦 Deploy to Production

### Render (Backend)
1. Push to GitHub
2. https://render.com → New Web Service
3. Build: `pip install -r backend/requirements.txt`
4. Start: `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add: `DATA_GOV_KEY` env variable

### Vercel (Frontend)
1. https://vercel.com → Import repo
2. Build: `npm run build`
3. Output: `dashboard/dist`
4. Add: `VITE_API_URL` env variable

---

## 🔧 Hardware Setup

### ESP32 Arduino Sketch

1. Arduino IDE → Tools → Manage Libraries
2. Search: `ArduinoJson` → Install
3. Open: `esp32_control/pralaya_esp32.ino`
4. Edit WiFi credentials (lines 24-25)
5. Board: ESP32 Dev Module
6. Upload

### GPIO Wiring

```
ESP32 PIN → COMPONENT
GPIO 21  → Green LED (+ resistor)
GPIO 22  → Red LED (+ resistor)
GPIO 23  → Buzzer
GND      → Common ground
```

---

## 📊 API Reference

### Health Check
```bash
GET /api/health
```

### Risk Alert (Hardware Integration)
```bash
GET /api/risk-alert
```
Response:
```json
{
  "risk_score": 0.85,
  "risk_level": "high",
  "hardware_trigger": {
    "buzzer": true,
    "red_led": true
  }
}
```

### Disaster Injection
```bash
POST /api/trigger/inject
Body: {"disaster_type": "flood", "severity": 0.85, "location": {"lat": X, "lon": Y}}
```

---

## ✅ Pre-Demo Checklist

```bash
# Backend
curl http://localhost:8000/api/health

# Frontend
curl http://localhost:5173

# API
curl -X POST http://localhost:8000/api/trigger/inject \
  -H "Content-Type: application/json" \
  -d '{"disaster_type":"flood","severity":0.85,"location":{"lat":28.6139,"lon":77.2090}}'

# ESP32 (if available)
# Monitor serial at 115200 baud
# Look for: "Risk Score: X | Level: Y"
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `backend/api/risk_alert_api.py` | Hardware alerts |
| `backend/middleware.py` | Rate limiting |
| `esp32_control/pralaya_esp32.ino` | Arduino sketch |
| `.env.example` | Config template |
| `README.md` | Full documentation |
| `DEPLOYMENT.md` | Deploy guide |
| `TESTING.md` | Test guide |

---

## 🔒 Security

✅ Rate limiting: 100 req/min
✅ Input validation: Type, severity, coordinates
✅ API key: Environment variable only
✅ Headers: XSS, CSRF, Clickjacking protection
✅ HTTPS: Ready for production

---

## ⚡ Performance

- API response: <300ms (with cache)
- Build time: <10 seconds
- Bundle size: <2MB
- Cache TTL: 30 seconds

---

## 🐛 Troubleshooting

### Backend won't start
```bash
python --version  # Check 3.8+
lsof -i :8000     # Check port
pip install -r requirements.txt --force-reinstall
```

### ESP32 won't connect
```bash
# Check WiFi credentials match
# Check serial at 115200 baud
# Check USB driver (CH340)
```

### Frontend can't reach backend
```bash
# Check CORS_ORIGINS in .env includes your URL
# Check backend is running
# Check firewall
```

---

## 📞 Documentation

- **Full README**: `README.md`
- **Deployment**: `DEPLOYMENT.md`
- **Testing**: `TESTING.md`
- **Architecture**: `docs/architecture.md`
- **API Docs**: http://localhost:8000/docs

---

## 🎯 Demo Scenario (5 mins)

1. **Start Systems** (Terminal 1-2)
   - Backend: `python -m uvicorn app:app --reload`
   - Dashboard: `npm run dev`

2. **Open Dashboard**
   - http://localhost:5173

3. **Inject Flood**
   ```bash
   curl -X POST http://localhost:8000/api/trigger/inject \
     -H "Content-Type: application/json" \
     -d '{"disaster_type":"flood","severity":0.85,"location":{"lat":28.6139,"lon":77.2090}}'
   ```

4. **Observe**
   - 🗺️ Red zone on map
   - 📈 Risk graph spikes
   - 🔔 ESP32 alert (if connected)

5. **Clear & Done**
   - Risk drops to 0
   - Green LED ON
   - Back to normal

---

## 📈 Next Steps

1. ✅ Run pre-demo checklist (see above)
2. ✅ Test disaster injection
3. ✅ Verify hardware (if available)
4. ✅ Practice demo flow
5. ✅ Deploy to Render + Vercel

---

**PRALAYA-NET v1.0** - Production Ready

Last Updated: February 5, 2026
