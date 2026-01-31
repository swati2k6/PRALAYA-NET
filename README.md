# PRALAYA-NET: Unified Disaster Command System

PRALAYA-NET bridges the gap between satellite surveillance and real-world action. Our project solves the problem of fragmented data and cascading infrastructure failures by using **Satellite AI (ViT)** to detect anomalies and **Graph Neural Networks (GNN)** to predict chain-reaction risks, like a flood leading to a power grid collapse.

## 🌟 Overview

PRALAYA-NET isn't just monitoring disasters; we're creating an automated, resilient brain that anticipates risks and coordinates an immediate response.

### Key Features

- **🧠 AI-Powered Decision Brain**: 
  - Vision Transformer (ViT) for satellite anomaly detection
  - LSTM for flood prediction
  - Graph Neural Networks (GNN) for cascading failure analysis
  - Space weather monitoring for GPS/communication failures

- **🖥️ Real-Time Command Dashboard**:
  - Live map visualization with disaster zones
  - Cascading risk graph visualization
  - Drone fleet monitoring and telemetry
  - Interactive control panel for disaster injection

- **🔌 Physical Edge Units**:
  - ESP32-based alert system with LEDs and buzzer
  - LCD display for critical alerts
  - WiFi-enabled for remote monitoring

- **🚁 Autonomous Drone Navigation**:
  - Visual SLAM (V-SLAM) for GPS-denied navigation
  - Real-time telemetry generation
  - Resilient operation during infrastructure failures

## 🏗️ Architecture

The system is split into three layers:

1. **Python Decision Brain** (`backend/`): Runs AI models, orchestration, and APIs
2. **React Command Dashboard** (`dashboard/`): Live mapping and situational awareness
3. **ESP32 Edge Unit** (`esp32_control/`): Hardware alerts and notifications

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- ESP32 board (optional)

### Setup

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app:app --reload --port 8000
   ```

2. **Dashboard**:
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```

3. **Access**:
   - Dashboard: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

See [SETUP.md](SETUP.md) for detailed setup instructions.

## 📖 Documentation

- [Architecture](docs/architecture.md) - System architecture explanation
- [Data Flow](docs/data-flow.md) - How data flows end-to-end
- [Cascading Risk](docs/cascading-risk.md) - Chain-reaction AI logic (GNN + LSTM + ViT)
- [Demo Script](docs/demo-script.md) - Exact demo steps

## 🎯 Demo Flow

1. Open the dashboard
2. Click "Inject Flood" in the Control Panel
3. Watch the system:
   - Detect the disaster via Satellite AI
   - Analyze cascading risks with GNN
   - Generate alerts and action plans
   - Deploy drones for reconnaissance
   - Send alerts to ESP32 edge units

## 📁 Project Structure

```
PRALAYA-NET/
├── backend/              # 🧠 Python Decision Brain
│   ├── ai/              # AI models (ViT, LSTM, GNN)
│   ├── api/             # FastAPI endpoints
│   ├── orchestration/   # Decision engine & alert manager
│   └── drone/           # Drone controller & telemetry
├── dashboard/            # 🖥️ React Command Dashboard
│   └── src/
│       ├── components/  # Map, Risk Graph, Drone Status, Control Panel
│       └── pages/       # Dashboard pages
├── drone_simulation/    # 🚁 V-SLAM demo
├── esp32_control/       # 🔌 ESP32 edge unit code
├── scripts/             # Utility scripts
├── data/                # Data storage
└── docs/                # Documentation
```

## 🛠️ Scripts

- `scripts/inject_disaster.py` - CLI tool to trigger disasters
- `scripts/mock_telemetry.py` - Generate fake drone telemetry
- `scripts/generate_graph.py` - Create cascading risk graphs

## 🔧 Technologies

- **Backend**: Python, FastAPI, NetworkX, PyTorch (simulated)
- **Frontend**: React, Leaflet, Vite
- **Hardware**: ESP32, MicroPython
- **AI**: Vision Transformers, LSTM, Graph Neural Networks

## 📝 License

MIT License

## 🙏 Acknowledgments

Built for hackathon demonstration. In production, this would integrate with:
- Real satellite data sources (Sentinel, Landsat, Bhuvan)
- Actual trained AI models
- Real drone APIs
- Production databases and infrastructure
