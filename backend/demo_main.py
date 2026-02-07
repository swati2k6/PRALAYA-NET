"""
PRALAYA-NET Demo Backend - Emergency Production Engine
Reliable backend for hackathon demo with guaranteed startup
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Create FastAPI app
app = FastAPI(
    title="PRALAYA-NET Demo Backend",
    version="1.0.0",
    description="Emergency Production Backend for Hackathon Demo"
)

# CORS Configuration - Allow all origins for demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Demo data storage
demo_data = {
    "system_status": "operational",
    "last_update": datetime.now().isoformat(),
    "risk_level": "medium",
    "stability_score": 0.75,
    "active_alerts": 3,
    "crisis_events": []
}

# Mock data generators
def generate_mock_risk_data():
    """Generate mock risk prediction data"""
    return {
        "risk_score": round(random.uniform(0.2, 0.8), 3),
        "risk_level": random.choice(["low", "medium", "high", "critical"]),
        "confidence": round(random.uniform(0.7, 0.95), 2),
        "factors": {
            "rainfall_weight": round(random.uniform(0.1, 0.4), 3),
            "earthquake_weight": round(random.uniform(0.0, 0.3), 3),
            "infrastructure_weight": round(random.uniform(0.2, 0.5), 3),
            "historical_weight": round(random.uniform(0.05, 0.15), 3)
        },
        "timestamp": datetime.now().isoformat()
    }

def generate_mock_stability_data():
    """Generate mock stability index data"""
    factors = {
        'infrastructure_health': random.uniform(0.6, 0.9),
        'disaster_risk': random.uniform(0.2, 0.5),
        'agent_response_capacity': random.uniform(0.7, 0.95),
        'temporal_stability': random.uniform(0.4, 0.8)
    }
    
    weights = {
        'infrastructure_health': 0.35,
        'disaster_risk': 0.30,
        'agent_response_capacity': 0.20,
        'temporal_stability': 0.15
    }
    
    overall_score = sum(factors[k] * weights[k] for k in factors)
    
    return {
        "stability_index": {
            "overall_score": round(overall_score, 3),
            "level": "excellent" if overall_score > 0.8 else "healthy" if overall_score > 0.6 else "warning",
            "factors": {k: round(v, 3) for k, v in factors.items()},
            "trend": random.choice(["improving", "stable", "declining"]),
            "timestamp": datetime.now().isoformat()
        }
    }

def generate_mock_alerts():
    """Generate mock active alerts"""
    alert_types = ["infrastructure_monitoring", "risk_assessment", "system_check", "autonomous_response"]
    alerts = []
    
    for i in range(random.randint(2, 5)):
        alerts.append({
            "alert_id": f"alert_{i}_{datetime.now().strftime('%H%M%S')}",
            "alert_type": random.choice(alert_types),
            "severity": random.choice(["info", "warning", "critical"]),
            "description": f"Autonomous {random.choice(alert_types)} in progress",
            "location": random.choice(["Mumbai", "Delhi", "Chennai", "Kolkata", "Bangalore"]),
            "progress": round(random.uniform(0.3, 0.9), 2),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 30))).isoformat()
        })
    
    return alerts

def generate_mock_timeline():
    """Generate mock crisis timeline events"""
    event_types = ["system_check", "agent_update", "risk_assessment", "infrastructure_alert", "autonomous_action"]
    events = []
    
    for i in range(random.randint(5, 10)):
        events.append({
            "event_id": f"event_{i}",
            "event_type": random.choice(event_types),
            "description": f"System performing {random.choice(event_types)}",
            "severity": random.choice(["info", "warning", "critical"]),
            "location": random.choice(["National", "Mumbai", "Delhi", "Chennai"]),
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 60))).isoformat()
        })
    
    return sorted(events, key=lambda x: x['timestamp'], reverse=True)

# Required endpoints
@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "PRALAYA-NET Demo Backend"
    }

@app.get("/api/health")
async def api_health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "api": "operational",
            "demo_mode": "active",
            "mock_data": "ready"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/demo/status")
async def demo_status():
    """Demo status endpoint"""
    return {
        "demo_mode": "active",
        "system_status": "operational",
        "backend_status": "online",
        "mock_data_available": True,
        "active_alerts": len(generate_mock_alerts()),
        "stability_score": demo_data["stability_score"],
        "last_update": datetime.now().isoformat()
    }

@app.get("/risk/predict")
async def predict_risk():
    """Risk prediction endpoint"""
    return generate_mock_risk_data()

@app.get("/api/risk/predict")
async def api_predict_risk():
    """API risk prediction endpoint"""
    return generate_mock_risk_data()

# Additional demo endpoints
@app.get("/api/stability/current")
async def get_current_stability():
    """Get current stability index"""
    return generate_mock_stability_data()

@app.get("/api/alerts/active")
async def get_active_alerts():
    """Get active alerts"""
    return {
        "alerts": generate_mock_alerts(),
        "total_count": len(generate_mock_alerts()),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/timeline/events")
async def get_timeline_events():
    """Get crisis timeline events"""
    return {
        "events": generate_mock_timeline(),
        "total_count": len(generate_mock_timeline()),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/system/status")
async def get_system_status():
    """Get comprehensive system status"""
    return {
        "backend_status": "online",
        "demo_mode": "active",
        "real_time_apis": {
            "status": "simulated",
            "sources": {
                "nasa_firms": "demo_mode",
                "usgs_earthquake": "demo_mode"
            }
        },
        "data_sources": {
            "real_time": ["demo_simulation"],
            "cached": ["mock_patterns"]
        },
        "services": {
            "stability_index": "active",
            "data_ingestion": "demo_mode",
            "prediction_engine": "active"
        },
        "timestamp": datetime.now().isoformat()
    }

# WebSocket endpoints for real-time demo
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    """General WebSocket endpoint"""
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(5)
            await websocket.send_json({
                "type": "ping",
                "timestamp": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"WebSocket error: {e}")

@app.websocket("/ws/risk-stream")
async def risk_stream_endpoint(websocket):
    """Risk data WebSocket stream"""
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(10)
            risk_data = generate_mock_risk_data()
            await websocket.send_json({
                "type": "risk_update",
                "data": risk_data
            })
    except Exception as e:
        print(f"Risk stream error: {e}")

@app.websocket("/ws/stability-stream")
async def stability_stream_endpoint(websocket):
    """Stability data WebSocket stream"""
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(10)
            stability_data = generate_mock_stability_data()
            await websocket.send_json({
                "type": "stability_update",
                "data": stability_data
            })
    except Exception as e:
        print(f"Stability stream error: {e}")

@app.websocket("/ws/actions-stream")
async def actions_stream_endpoint(websocket):
    """Actions data WebSocket stream"""
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(15)
            alerts = generate_mock_alerts()
            if alerts:
                await websocket.send_json({
                    "type": "action_update",
                    "data": alerts[0]  # Send latest alert
                })
    except Exception as e:
        print(f"Actions stream error: {e}")

@app.websocket("/ws/timeline-stream")
async def timeline_stream_endpoint(websocket):
    """Timeline data WebSocket stream"""
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(20)
            events = generate_mock_timeline()
            if events:
                await websocket.send_json({
                    "type": "event",
                    "data": events[0]  # Send latest event
                })
    except Exception as e:
        print(f"Timeline stream error: {e}")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PRALAYA-NET Demo Backend",
        "status": "operational",
        "version": "1.0.0",
        "demo_mode": "active",
        "endpoints": {
            "health": "/health",
            "api_health": "/api/health",
            "demo_status": "/demo/status",
            "risk_predict": "/risk/predict",
            "api_risk_predict": "/api/risk/predict",
            "stability": "/api/stability/current",
            "alerts": "/api/alerts/active",
            "timeline": "/api/timeline/events"
        }
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__,
            "timestamp": datetime.now().isoformat(),
            "demo_mode": "active"
        }
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("🚀 Starting PRALAYA-NET Demo Backend...")
    print(f"📍 Server: http://0.0.0.0:{port}")
    print(f"📍 Health: http://127.0.0.1:{port}/health")
    print(f"📍 Demo Status: http://127.0.0.1:{port}/demo/status")
    print(f"📍 Risk Predict: http://127.0.0.1:{port}/risk/predict")
    print("🎯 DEMO MODE ACTIVE - Mock Data Ready")

    uvicorn.run(
        "demo_main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload for stability
        log_level="info"
    )
