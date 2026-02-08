# PRALAYA-NET Autonomous Drone Operations Dashboard - Implementation Plan

## Overview
Upgrade PRALAYA-NET into a fully working software-simulated autonomous drone operations dashboard.

## Tasks

### Phase 1: Backend Enhancements
- [ ] 1.1 Enhance drone_fleet_api.py with real-time safe drone count calculation
- [ ] 1.2 Integrate OpenWeather API with weather-based drone limits
- [ ] 1.3 Add NASA satellite data fallback for GPS positioning
- [ ] 1.4 Implement prediction module with ≥90% confidence scoring
- [ ] 1.5 Add Data.gov historical data integration for risk prediction

### Phase 2: Frontend Services
- [ ] 2.1 Update api.js with drone fleet API endpoints
- [ ] 2.2 Add safe-drone-count endpoint integration
- [ ] 2.3 Enhance geoIntelligenceService.js with prediction module calls

### Phase 3: Interactive Map Enhancements
- [ ] 3.1 Update MapView.jsx with click-to-fetch weather/risk/safe-count
- [ ] 3.2 Enhance RiskPopup.jsx to display safe drone count
- [ ] 3.3 Add live weather, geolocation, and hazard data display

### Phase 4: Drone View Simulation
- [ ] 4.1 Create DroneView.jsx with 12-panel camera feed
- [ ] 4.2 Implement WebRTC/MediaStream camera permission
- [ ] 4.3 Add real-time feed replication across all panels
- [ ] 4.4 Create "Launch Drone View" button functionality

### Phase 5: UI Enhancements
- [ ] 5.1 Beautify navbar with Tailwind CSS styling
- [ ] 5.2 Improve responsive dashboard layout
- [ ] 5.3 Add mode indicators and status displays
- [ ] 5.4 Fix any white-screen or routing errors

### Phase 6: Deployment Readiness
- [ ] 6.1 Ensure backend runs on Render (Python 3.12)
- [ ] 6.2 Configure frontend for Netlify/Vercel
- [ ] 6.3 Verify environment variables setup
- [ ] 6.4 Test backend-frontend connectivity

## Implementation Order
1. Backend enhancements (drone_fleet_api.py)
2. Frontend services (api.js)
3. Map and popup components
4. Drone view component
5. App navigation updates
6. UI styling improvements
7. Deployment configuration

## Success Criteria
- ✓ Click map anywhere → Get live weather, risk level, safe drone count
- ✓ Launch Drone View → 12-panel camera feed with device camera
- ✓ Safe drone count based on real-time weather/wind/risk
- ✓ ≥90% predictive confidence scoring
- ✓ Beautiful responsive Tailwind UI
- ✓ Deployment-ready for Render/Netlify

