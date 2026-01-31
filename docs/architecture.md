# PRALAYA-NET Architecture

## Overview

PRALAYA-NET is a multi-layered disaster management system integrating AI, real-time monitoring, and hardware control.

## Layers

### 1. Data Layer
- **Raw Data**: Satellite images, sensor feeds
- **Processed Data**: AI model inputs/outputs
- **Simulated Data**: Mock scenarios for testing

### 2. AI Layer (Backend)
- **Satellite AI**: ViT model for anomaly detection
- **Flood Predictor**: LSTM for time-series prediction
- **Graph Risk**: GNN for cascading failure analysis
- **Space Weather**: Additional environmental factors

### 3. Orchestration Layer
- **Decision Engine**: Combines AI outputs, triggers actions
- **Alert Manager**: Sends alerts to dashboard and ESP32

### 4. API Layer
- **Trigger API**: Inject disasters
- **Drone API**: Control and monitor drones
- **Satellite API**: Fetch satellite data

### 5. Frontend Layer (Dashboard)
- **Map View**: Leaflet map with disaster zones
- **Risk Graph**: Network visualization of cascading risks
- **Control Panel**: Buttons to inject disasters
- **Drone Status**: Real-time telemetry

### 6. Hardware Layer
- **Drone Simulation**: Generates telemetry, V-SLAM navigation
- **ESP32 Control**: LCD, buzzer, LED alerts

## Data Flow

1. Satellite images → AI models → Risk assessment
2. Decision engine → Alerts → Dashboard + ESP32
3. Drone telemetry → Dashboard visualization
4. User input (dashboard) → Backend APIs → Actions

## Technologies

- Backend: Python, FastAPI, NetworkX
- Frontend: React, Leaflet, Vite
- AI: PyTorch (simulated)
- Hardware: ESP32 (MicroPython), Drone simulation (Python)
