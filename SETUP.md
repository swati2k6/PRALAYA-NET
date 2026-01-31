# PRALAYA-NET Setup Guide

Complete setup instructions for the PRALAYA-NET disaster management system.

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- ESP32 board (optional, for hardware alerts)
- Webcam or video file (optional, for drone SLAM demo)

## Quick Start

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 2. Dashboard Setup

```bash
cd dashboard
npm install
npm run dev
```

Dashboard will be available at `http://localhost:5173` (or similar Vite port)

### 3. Test the System

1. Open the dashboard in your browser
2. Click "Inject Flood" in the Control Panel
3. Watch the map update and risk graph populate
4. Check drone status for telemetry updates

## Detailed Setup

### Backend Configuration

Edit `backend/config.py` to customize:
- Risk thresholds
- Critical infrastructure locations
- ESP32 IP address
- Data paths

### Dashboard Configuration

Edit `dashboard/src/services/api.js` to change:
- Backend API URL (if not running on localhost:8000)

### ESP32 Setup

1. Install MicroPython on ESP32
2. Upload `esp32_control/main.py` to ESP32
3. Update WiFi credentials in the code:
   ```python
   WIFI_SSID = "YOUR_WIFI_SSID"
   WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
   ```
4. Update backend URL if needed
5. Wire components according to `esp32_control/wiring_diagram.md`
6. Power on ESP32 and check serial monitor

### Drone Simulation

```bash
cd drone_simulation
python visual_slam.py
```

- Press `s` to enable/disable SLAM
- Press `q` to quit
- Requires webcam or video file

## API Endpoints

### Backend APIs

- `GET /` - Health check
- `GET /api/health` - System health
- `POST /api/trigger/disaster` - Trigger disaster
- `GET /api/trigger/status` - System status
- `POST /api/trigger/clear` - Clear all disasters
- `GET /api/drones/status` - Drone fleet status
- `GET /api/drones/telemetry/{drone_id}` - Drone telemetry
- `GET /api/satellite/zones` - Disaster zones
- `GET /api/orchestration/alerts/esp32` - ESP32 alerts

## Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify all dependencies are installed
- Check Python version (3.8+)

### Dashboard won't load
- Ensure backend is running
- Check browser console for errors
- Verify API URL in `api.js`

### ESP32 not connecting
- Verify WiFi credentials
- Check backend URL and network connectivity
- Ensure ESP32 and backend are on same network

### Map not displaying
- Check internet connection (Leaflet requires online tiles)
- Verify Leaflet CSS is loaded
- Check browser console for errors

## Development

### Running Tests

```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd dashboard
npm test
```

### Project Structure

```
PRALAYA-NET/
├── backend/          # Python FastAPI backend
├── dashboard/        # React dashboard
├── drone_simulation/ # V-SLAM demo
├── esp32_control/    # ESP32 code
├── scripts/          # Utility scripts
├── data/             # Data storage
└── docs/             # Documentation
```

## Next Steps

1. Add real satellite data sources
2. Train actual AI models (ViT, LSTM, GNN)
3. Integrate real drone APIs
4. Add database for persistence
5. Implement WebSocket for real-time updates
6. Add authentication and security

## Support

For issues or questions, check:
- `docs/architecture.md` - System architecture
- `docs/data-flow.md` - Data flow explanation
- `docs/demo-script.md` - Demo walkthrough



