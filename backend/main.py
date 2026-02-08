"""
PRALAYA-NET Backend - Main Entry Point
Complete FastAPI application with all API integrations for disaster management
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uvicorn
import os
import asyncio
import httpx
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configuration
from config import (
    APP_NAME, VERSION, PORT, CORS_ORIGINS,
    NASA_API_KEY, DATA_GOV_KEY, OPENWEATHER_API_KEY, DEMO_MODE,
    NASA_POWER_URL, OPENWEATHER_URL, USGS_EARTHQUAKE_URL,
    CRITICAL_INFRA, LOW_RISK, MEDIUM_RISK, HIGH_RISK, CRITICAL_RISK
)

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="Autonomous Disaster Response Command Platform - AI-powered disaster prediction and response"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============== Pydantic Models ==============

class WeatherResponse(BaseModel):
    location: Dict[str, float]
    temperature: float
    humidity: int
    wind_speed: float
    wind_direction: int
    description: str
    visibility: int
    clouds: int
    timestamp: str

class GeoIntelResponse(BaseModel):
    coordinates: Dict[str, float]
    weather: Optional[Dict[str, Any]] = None
    nasa_data: Optional[Dict[str, Any]] = None
    infrastructure: List[Dict[str, Any]] = []
    risk_score: float
    risk_level: str
    timestamp: str

class InfrastructureResponse(BaseModel):
    facilities: List[Dict[str, Any]]
    total_count: int
    timestamp: str

# ============== Utility Functions ==============

async def fetch_openweather(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Fetch weather data from OpenWeather API"""
    if not OPENWEATHER_API_KEY or DEMO_MODE:
        # Return simulated data
        return {
            "name": "Demo Location",
            "main": {
                "temp": 25 + (lat * 10) % 10,
                "humidity": int(50 + (lon * 5) % 40),
                "pressure": 1013 + int((lat + lon) % 20)
            },
            "wind": {
                "speed": 3 + (lat + lon) % 10,
                "deg": int((lon * 10) % 360)
            },
            "weather": [{"description": "Partly cloudy", "main": "Clouds"}],
            "clouds": {"all": int((lat + lon) % 100)},
            "visibility": 10000
        }
    
    try:
        async with httpx.AsyncClient() as client:
            url = f"{OPENWEATHER_URL}?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"OpenWeather API error: {response.status_code}")
                return None
    except Exception as e:
        print(f"OpenWeather request failed: {e}")
        return None

async def fetch_nasa_power(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Fetch climate data from NASA POWER API"""
    if DEMO_MODE:
        # Return simulated data
        return {
            "temperature": 25 + (lat * 5) % 15,
            "precipitation": (lon * 2) % 10,
            "solar_radiation": 500 + (lat + lon) % 300,
            "relative_humidity": 50 + (lon * 3) % 40
        }
    
    try:
        async with httpx.AsyncClient() as client:
            params = {
                "parameters": "T2M,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN",
                "community": "RE",
                "longitude": lon,
                "latitude": lat,
                "format": "JSON"
            }
            response = await client.get(NASA_POWER_URL, params=params, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                properties = data.get("properties", {}).get("parameter", {})
                times = sorted(properties.get("T2M", {}).keys())
                if times:
                    latest = times[-1]
                    return {
                        "temperature": properties.get("T2M", {}).get(latest, 25),
                        "precipitation": properties.get("PRECTOTCORR", {}).get(latest, 0),
                        "solar_radiation": properties.get("ALLSKY_SFC_SW_DWN", {}).get(latest, 500),
                        "relative_humidity": properties.get("RH2M", {}).get(latest, 50)
                    }
            return None
    except Exception as e:
        print(f"NASA POWER API error: {e}")
        return None

def calculate_risk_score(weather: Dict, nasa: Dict) -> float:
    """Calculate AI risk score based on weather and NASA data"""
    score = 0
    
    if weather:
        # Wind Score (up to 40 points)
        wind_speed = weather.get("wind", {}).get("speed", 0)
        if wind_speed > 14:
            score += 40
        elif wind_speed > 8:
            score += 20
        elif wind_speed > 4:
            score += 10
        
        # Rainfall Score (up to 30 points)
        rain_1h = weather.get("rain", {}).get("1h", 0)
        if rain_1h > 10:
            score += 30
        elif rain_1h > 2:
            score += 15
        
        # Temperature Score (up to 15 points)
        temp = weather.get("main", {}).get("temp", 20)
        if temp > 40 or temp < -5:
            score += 15
        
        # Condition Score (up to 15 points)
        condition = weather.get("weather", [{}])[0].get("main", "").lower()
        severe_conditions = ["thunderstorm", "tornado", "extreme", "hurricane", "cyclone"]
        if any(c in condition for c in severe_conditions):
            score += 15
    
    if nasa:
        # NASA precipitation anomaly (up to 20 points)
        precip = nasa.get("precipitation", 0)
        if precip > 10:
            score += 20
        elif precip > 5:
            score += 10
    
    return min(score, 100)

def get_risk_level(score: float) -> str:
    """Convert risk score to risk level"""
    if score >= 80:
        return "critical"
    elif score >= 60:
        return "high"
    elif score >= 40:
        return "elevated"
    elif score >= 20:
        return "moderate"
    return "low"

# ============== API Endpoints ==============

@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "online",
        "system": APP_NAME,
        "version": VERSION,
        "message": "PRALAYA-NET backend is operational",
        "demo_mode": DEMO_MODE,
        "endpoints": {
            "health": "/api/health",
            "weather": "/api/weather?lat=&lon=",
            "geo_intel": "/api/geo-intel?lat=&lon=",
            "infrastructure": "/api/infrastructure",
            "risk_prediction": "/api/risk/predict",
            "stability": "/api/stability/current"
        }
    }

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": APP_NAME,
        "version": VERSION
    }

@app.get("/api/health")
async def api_health_check():
    """Detailed API health check"""
    return {
        "status": "healthy",
        "components": {
            "api": "operational",
            "websocket": "ready",
            "demo_mode": DEMO_MODE
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/weather")
async def get_weather(lat: float = Query(..., description="Latitude"),
                      lon: float = Query(..., description="Longitude")):
    """
    Get current weather for a location
    
    Uses OpenWeather API when API key is available.
    Falls back to simulated data in demo mode.
    """
    weather_data = await fetch_openweather(lat, lon)
    
    if not weather_data:
        raise HTTPException(status_code=503, detail="Unable to fetch weather data")
    
    return {
        "location": {"lat": lat, "lon": lon},
        "temperature": weather_data.get("main", {}).get("temp", 0),
        "humidity": weather_data.get("main", {}).get("humidity", 0),
        "wind_speed": weather_data.get("wind", {}).get("speed", 0),
        "wind_direction": weather_data.get("wind", {}).get("deg", 0),
        "description": weather_data.get("weather", [{}])[0].get("description", "Unknown"),
        "visibility": weather_data.get("visibility", 0),
        "clouds": weather_data.get("clouds", {}).get("all", 0),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/geo-intel")
async def get_geo_intel(lat: float = Query(..., description="Latitude"),
                        lon: float = Query(..., description="Longitude")):
    """
    Get comprehensive geo-intelligence for a location
    
    Combines weather, NASA climate data, and infrastructure information.
    Returns AI-calculated risk score for disaster assessment.
    """
    # Fetch data from multiple sources in parallel
    weather, nasa_data = await asyncio.gather(
        fetch_openweather(lat, lon),
        fetch_nasa_power(lat, lon)
    )
    
    # Calculate risk score
    risk_score = calculate_risk_score(weather, nasa_data)
    
    # Find nearby infrastructure
    nearby_infra = []
    for facility in CRITICAL_INFRA:
        import math
        dist = math.sqrt(
            (facility["lat"] - lat)**2 + (facility["lon"] - lon)**2
        )
        if dist < 0.5:  # Within ~50km
            nearby_infra.append({
                **facility,
                "distance_km": round(dist * 111, 2)
            })
    
    return {
        "coordinates": {"lat": lat, "lon": lon},
        "weather": weather,
        "nasa_data": nasa_data,
        "infrastructure": nearby_infra,
        "risk_score": risk_score,
        "risk_level": get_risk_level(risk_score),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/infrastructure")
async def get_infrastructure(lat: Optional[float] = Query(None),
                            lon: Optional[float] = Query(None)):
    """
    Get critical infrastructure data
    
    Returns all registered infrastructure facilities.
    Optionally filters by proximity to given coordinates.
    """
    if lat is not None and lon is not None:
        # Calculate distances and sort by proximity
        import math
        for facility in CRITICAL_INFRA:
            dist = math.sqrt(
                (facility["lat"] - lat)**2 + (facility["lon"] - lon)**2
            )
            facility["distance_km"] = round(dist * 111, 2)
        
        facilities = sorted(CRITICAL_INFRA, key=lambda x: x.get("distance_km", 999))
    else:
        facilities = CRITICAL_INFRA
    
    return {
        "facilities": facilities,
        "total_count": len(facilities),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/risk/predict")
async def predict_risk(lat: Optional[float] = Query(None),
                       lon: Optional[float] = Query(None)):
    """
    Lightweight risk prediction endpoint
    
    Returns risk assessment based on available data.
    Uses simulated data when APIs are unavailable.
    """
    if lat is None:
        lat = 28.6139
    if lon is None:
        lon = 77.2090
    
    # Fetch available data
    weather = await fetch_openweather(lat, lon)
    nasa = await fetch_nasa_power(lat, lon)
    
    risk_score = calculate_risk_score(weather, nasa)
    
    # Generate risk factors
    factors = {
        "wind_contribution": min(weather.get("wind", {}).get("speed", 0) * 2, 40) if weather else 0,
        "rainfall_contribution": weather.get("rain", {}).get("1h", 0) * 2 if weather else 0,
        "temperature_anomaly": abs(weather.get("main", {}).get("temp", 25) - 25) * 0.5 if weather else 0,
        "nasa_precipitation_anomaly": (nasa.get("precipitation", 0) * 2) if nasa else 0
    }
    
    return {
        "risk_score": round(risk_score, 2),
        "risk_level": get_risk_level(risk_score),
        "confidence": 0.85 if not DEMO_MODE else 0.7,
        "factors": factors,
        "coordinates": {"lat": lat, "lon": lon},
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/stability/current")
async def get_current_stability():
    """Get current system stability index"""
    import random
    
    factors = {
        'infrastructure_health': round(random.uniform(0.6, 0.9), 3),
        'disaster_risk': round(random.uniform(0.2, 0.5), 3),
        'agent_response_capacity': round(random.uniform(0.7, 0.95), 3),
        'temporal_stability': round(random.uniform(0.4, 0.8), 3)
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
            "factors": factors,
            "trend": random.choice(["improving", "stable", "declining"]),
            "timestamp": datetime.now().isoformat()
        }
    }

@app.get("/api/system-status")
async def get_system_status():
    """Get comprehensive system status"""
    return {
        "backend_status": "online",
        "demo_mode": DEMO_MODE,
        "real_time_apis": {
            "status": "online" if not DEMO_MODE else "demo",
            "openweather": "connected" if OPENWEATHER_API_KEY else "demo_mode",
            "nasa_power": "connected" if not DEMO_MODE else "demo_mode",
            "usgs_earthquake": "connected"
        },
        "services": {
            "stability_index": "enhanced",
            "data_ingestion": "active",
            "prediction_engine": "enhanced" if not DEMO_MODE else "basic"
        },
        "timestamp": datetime.now().isoformat()
    }

# ============== WebSocket Endpoints ==============

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
            risk_data = await predict_risk()
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
            stability_data = await get_current_stability()
            await websocket.send_json({
                "type": "stability_update",
                "data": stability_data
            })
    except Exception as e:
        print(f"Stability stream error: {e}")

# ============== Exception Handler ==============

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "type": type(exc).__name__,
            "timestamp": datetime.now().isoformat()
        }
    )

# ============== Main Entry Point ==============

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 PRALAYA-NET Backend Starting...")
    print("="*70)
    print(f"📍 Server: http://0.0.0.0:{PORT}")
    print(f"📍 Local:  http://127.0.0.1:{PORT}")
    print(f"📍 Docs:   http://127.0.0.1:{PORT}/docs")
    print(f"📍 Health: http://127.0.0.1:{PORT}/health")
    print(f"📍 Demo Mode: {DEMO_MODE}")
    print("="*70 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True,
        log_level="info"
    )

