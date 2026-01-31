# PRALAYA-NET Demo Script

## Pre-Demo Setup

1. **Start Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app:app --reload --port 8000
   ```

2. **Start Dashboard**:
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```

3. **Verify ESP32** (optional):
   - Upload `esp32_control/main.py` to ESP32
   - Connect to WiFi network
   - ESP32 will poll backend for alerts

## Demo Flow (5-10 minutes)

### Step 1: Introduction (30 seconds)
- "PRALAYA-NET bridges satellite surveillance with real-world action"
- "We use AI to detect anomalies and predict cascading infrastructure failures"
- "Our system has three layers: Python Decision Brain, React Dashboard, and ESP32 Edge Unit"

### Step 2: Show Dashboard (1 minute)
- Point to map: "This is our live situational awareness map"
- Show Risk Graph: "This visualizes cascading failure risks using Graph Neural Networks"
- Show Drone Status: "We're simulating autonomous drone navigation with V-SLAM"

### Step 3: Inject Flood Disaster (2 minutes)
- Click "Inject Flood" button in Control Panel
- **What to say**: "We're simulating a flood detected by satellite AI"
- Watch map update with flood zone
- Watch Risk Graph show cascading risks:
  - "Flood → Power Grid (risk increasing)"
  - "Power Grid → Hospital (critical infrastructure at risk)"
  - "Water Supply → Telecom Tower (communication infrastructure threatened)"

### Step 4: Show AI Predictions (2 minutes)
- Point to risk scores on graph nodes
- **What to say**: "Our GNN model predicts that this flood will cause a power grid collapse in 15 minutes, which will then impact the hospital"
- Show how risks propagate through the network
- Mention: "This is where our Decision Brain kicks in"

### Step 5: Show Automated Response (2 minutes)
- Point to alerts appearing
- **What to say**: "The Decision Engine automatically triggered alerts to the ESP32 edge unit"
- Show ESP32 (if available): LCD showing alert, buzzer beeping, LED flashing
- Mention: "We're also sending commands to deploy drones for reconnaissance"

### Step 6: Show Drone V-SLAM (1 minute)
- Point to Drone Status component
- **What to say**: "Our drones use Visual SLAM for navigation, so they can operate even if GPS fails during a crisis"
- Show telemetry updating (altitude, position, battery)
- Mention: "This proves our system is resilient to infrastructure failures"

### Step 7: Inject Second Disaster (1 minute)
- Click "Inject Fire" button
- Show how system handles multiple simultaneous disasters
- Point to how cascading risks combine

### Step 8: Closing (30 seconds)
- "PRALAYA-NET isn't just monitoring disasters; we're creating an automated, resilient brain that anticipates risks and coordinates immediate response"
- "Our system uses Satellite AI (ViT), Flood Prediction (LSTM), and Cascading Risk Analysis (GNN) to make intelligent decisions"

## Key Talking Points

- **Problem**: Fragmented data, cascading infrastructure failures
- **Solution**: Unified system with AI-powered prediction and automated response
- **Innovation**: V-SLAM for GPS-denied navigation, GNN for cascading failure prediction
- **Impact**: Real-time decision-making saves lives and prevents infrastructure collapse

## Troubleshooting

- If backend doesn't start: Check port 8000 is free
- If dashboard doesn't load: Check backend is running
- If ESP32 doesn't connect: Verify WiFi credentials in `esp32_control/main.py`
- If graph doesn't update: Check browser console for errors

## Demo Checklist

- [ ] Backend running on port 8000
- [ ] Dashboard accessible (usually http://localhost:5173)
- [ ] Map loads correctly
- [ ] Control Panel buttons work
- [ ] Risk Graph displays
- [ ] Drone Status shows telemetry
- [ ] ESP32 connected (optional)
- [ ] Sample disaster scenarios in `data/simulated/`



