# Data Flow in PRALAYA-NET

## Data Sources

- **Satellite Images**: Raw TIFF files in `data/raw/`
- **Sensor Data**: ESP32 sensors, drone telemetry
- **Simulated Data**: Mock disasters in `data/simulated/`

## Processing Pipeline

1. **Ingestion**: Raw data loaded into backend
2. **Preprocessing**: Normalization, feature extraction → `data/processed/`
3. **AI Inference**: Models predict risks
4. **Orchestration**: Combine predictions, decide actions
5. **Output**: Alerts to dashboard and ESP32

## API Endpoints

- `POST /trigger`: Inject disaster
- `GET /drones/status`: Fetch telemetry
- `GET /satellite/zones`: Get detected zones

## Real-Time Updates

- WebSocket or polling for live data
- Dashboard updates every 5 seconds
- ESP32 polls backend for alerts

## Storage

- In-memory for demo (extend to database for production)
- Logs saved to files for auditing

## Security

- Basic auth for APIs (demo only)
- HTTPS recommended for production
