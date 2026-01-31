"""
Satellite API - Fetch satellite data and weather information
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
import random
import json
from datetime import datetime
from config import DATA_SIMULATED_PATH
import os

router = APIRouter()

# Global storage for disaster zones (shared with decision engine)
satellite_zones: List[Dict] = []
weather_data = {}

@router.get("/zones")
async def get_satellite_zones():
    """
    Get detected disaster zones from satellite imagery
    Returns zones detected by ViT model
    """
    return {
        "zones": satellite_zones,
        "timestamp": datetime.now().isoformat(),
        "count": len(satellite_zones)
    }

@router.post("/zones")
async def add_satellite_zone(zone: Dict):
    """
    Add a new disaster zone (called by AI models)
    """
    zone["id"] = zone.get("id", f"zone_{len(satellite_zones) + 1}")
    zone["detected_at"] = zone.get("detected_at", datetime.now().isoformat())
    satellite_zones.append(zone)
    return {"status": "added", "zone_id": zone["id"]}

@router.get("/weather")
async def get_weather_data(lat: float = 28.6139, lon: float = 77.2090):
    """
    Get weather data for a location
    Mock implementation - in production, call real weather API
    """
    location_key = (round(lat, 2), round(lon, 2))
    
    if location_key not in weather_data:
        weather_data[location_key] = {
            "temperature": round(random.uniform(20, 35), 1),
            "humidity": round(random.uniform(40, 90), 1),
            "wind_speed": round(random.uniform(5, 25), 1),
            "precipitation": round(random.uniform(0, 50), 1),
            "pressure": round(random.uniform(1000, 1020), 1),
            "timestamp": datetime.now().isoformat()
        }
    
    return weather_data[location_key]

@router.get("/anomalies")
async def get_anomalies():
    """
    Get detected anomalies from satellite AI
    """
    # Return zones as anomalies for now
    anomalies = []
    for zone in satellite_zones:
        anomalies.append({
            "id": zone.get("id"),
            "type": zone.get("type", "unknown"),
            "confidence": zone.get("severity", 0.7),
            "location": zone.get("location", {}),
            "detected_at": zone.get("detected_at", datetime.now().isoformat())
        })
    
    return {
        "anomalies": anomalies,
        "count": len(anomalies),
        "timestamp": datetime.now().isoformat()
    }

@router.delete("/zones/{zone_id}")
async def clear_zone(zone_id: str):
    """Clear a specific zone"""
    global satellite_zones
    satellite_zones = [z for z in satellite_zones if z.get("id") != zone_id]
    return {"status": "cleared", "zone_id": zone_id}

@router.delete("/zones")
async def clear_all_zones():
    """Clear all zones"""
    global satellite_zones
    satellite_zones.clear()
    return {"status": "all_cleared"}
