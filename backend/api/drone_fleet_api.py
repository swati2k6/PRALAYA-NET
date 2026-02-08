"""
Drone Fleet API - Autonomous Drone Operations Management
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
import random
import math

router = APIRouter()

# ============== Drone Fleet Configuration ==============

class DroneFleetConfig:
    """Drone fleet configuration and state"""
    
    # Fleet size
    TOTAL_DRONES = 12
    
    # Drone types and their capabilities
    DRONE_TYPES = {
        "surveillance": {
            "max_wind": 35,
            "max_precipitation": 10,
            "min_temp": -10,
            "max_temp": 50,
            "battery_life": 45,
        },
        "delivery": {
            "max_wind": 25,
            "max_precipitation": 5,
            "min_temp": 0,
            "max_temp": 45,
            "battery_life": 30,
        },
        "rescue": {
            "max_wind": 45,
            "max_precipitation": 15,
            "min_temp": -20,
            "max_temp": 55,
            "battery_life": 60,
        }
    }
    
    def __init__(self):
        self.fleet_status = self._initialize_fleet()
    
    def _initialize_fleet(self) -> List[Dict]:
        """Initialize fleet with drone states"""
        drones = []
        for i in range(self.TOTAL_DRONES):
            drones.append({
                "id": f"DRONE-{i+1:03d}",
                "type": list(self.DRONE_TYPES.keys())[i % 3],
                "status": "available",
                "battery": random.randint(70, 100),
                "altitude": 0,
                "speed": 0,
                "heading": random.randint(0, 360),
                "location": {"lat": None, "lon": None},
                "slam_enabled": True,
                "last_update": datetime.now().isoformat()
            })
        return drones
    
    def get_fleet_status(self) -> Dict:
        """Get current fleet status"""
        available = len([d for d in self.fleet_status if d["status"] == "available"])
        active = len([d for d in self.fleet_status if d["status"] == "active"])
        charging = len([d for d in self.fleet_status if d["status"] == "charging"])
        maintenance = len([d for d in self.fleet_status if d["status"] == "maintenance"])
        
        return {
            "total_drones": self.TOTAL_DRONES,
            "available": available,
            "active": active,
            "charging": charging,
            "maintenance": maintenance,
            "drones": self.fleet_status,
            "timestamp": datetime.now().isoformat()
        }
    
    def calculate_safe_drone_count(self, weather: Dict, risk_score: float, location: Dict) -> Dict:
        """
        Calculate safe number of drones for deployment based on conditions
        """
        lat = location.get("lat", 0)
        lon = location.get("lon", 0)
        
        # Extract weather data
        wind_speed = weather.get("wind", {}).get("speed", 0) * 3.6
        precipitation = weather.get("rain", {}).get("1h", 0)
        temperature = weather.get("main", {}).get("temp", 25)
        visibility = weather.get("visibility", 10000)
        
        # Risk-based factors
        risk_factor = max(0, 1 - (risk_score / 100))
        
        # Wind factor
        if wind_speed < 10:
            wind_factor = 1.0
        elif wind_speed < 25:
            wind_factor = 0.7
        elif wind_speed < 35:
            wind_factor = 0.4
        else:
            wind_factor = 0.1
        
        # Precipitation factor
        if precipitation < 2:
            precip_factor = 1.0
        elif precipitation < 10:
            precip_factor = 0.6
        else:
            precip_factor = 0.2
        
        # Temperature factor
        if -10 <= temperature <= 45:
            temp_factor = 1.0
        elif -20 <= temperature < -10 or 45 < temperature <= 55:
            temp_factor = 0.7
        else:
            temp_factor = 0.3
        
        # Visibility factor
        visibility_factor = min(1.0, visibility / 5000)
        
        # Calculate safe count
        safe_count = int(
            self.TOTAL_DRONES * 
            risk_factor * 
            wind_factor * 
            precip_factor * 
            temp_factor * 
            visibility_factor
        )
        
        safe_count = max(0, min(self.TOTAL_DRONES, safe_count))
        
        # Generate recommendations
        recommendations = []
        if wind_speed > 25:
            recommendations.append({
                "type": "warning",
                "message": f"High wind speed ({wind_speed:.1f} km/h) - Limit surveillance drones"
            })
        if precipitation > 5:
            recommendations.append({
                "type": "warning",
                "message": f"Precipitation detected ({precipitation}mm) - Use waterproof drones only"
            })
        if risk_score > 70:
            recommendations.append({
                "type": "critical",
                "message": f"High risk area - Reduce drone deployment by 50%"
            })
        if visibility < 3000:
            recommendations.append({
                "type": "warning",
                "message": f"Low visibility ({visibility}m) - Enable V-SLAM navigation"
            })
        if not recommendations:
            recommendations.append({
                "type": "info",
                "message": "Conditions optimal for full drone deployment"
            })
        
        return {
            "safe_drone_count": safe_count,
            "max_drones": self.TOTAL_DRONES,
            "factors": {
                "risk_factor": round(risk_factor, 2),
                "wind_factor": round(wind_factor, 2),
                "precipitation_factor": round(precip_factor, 2),
                "temperature_factor": round(temp_factor, 2),
                "visibility_factor": round(visibility_factor, 2)
            },
            "conditions": {
                "wind_speed_kmh": round(wind_speed, 1),
                "precipitation_mm": round(precipitation, 1),
                "temperature_c": round(temperature, 1),
                "visibility_m": round(visibility, 0),
                "risk_score": risk_score
            },
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
    
    def estimate_position_without_gps(self, lat: float, lon: float, weather: Dict) -> Dict:
        """
        Estimate drone position using satellite/weather data when GPS unavailable
        """
        wind = weather.get("wind", {})
        wind_speed = wind.get("speed", 0)
        wind_deg = wind.get("deg", 0)
        
        # Estimate drift based on wind
        drift_lat = (wind_speed * 0.001 * math.sin(math.radians(wind_deg)))
        drift_lon = (wind_speed * 0.001 * math.cos(math.radians(wind_deg)))
        
        estimated_lat = lat + drift_lat
        estimated_lon = lon + drift_lon
        
        visibility = weather.get("visibility", 10000)
        confidence = min(0.95, visibility / 10000)
        
        return {
            "estimated_location": {
                "lat": round(estimated_lat, 6),
                "lon": round(estimated_lon, 6)
            },
            "gps_status": "unavailable",
            "fallback_method": "satellite_weather_estimation",
            "confidence": round(confidence, 2),
            "drift_compensation": {
                "lat_drift": round(drift_lat, 6),
                "lon_drift": round(drift_lon, 6)
            },
            "slam_recommended": visibility < 5000,
            "timestamp": datetime.now().isoformat()
        }


# Global fleet instance
drone_fleet = DroneFleetConfig()


# ============== API Models ==============

class DroneDeployRequest(BaseModel):
    drone_id: str
    target_lat: float
    target_lon: float
    mission_type: str = "surveillance"
    altitude: int = 100


class DronePositionEstimate(BaseModel):
    lat: float
    lon: float
    weather_data: Optional[Dict] = None


# ============== API Endpoints ==============

@router.get("/api/drones/fleet-status")
async def get_fleet_status():
    """Get complete drone fleet status"""
    return drone_fleet.get_fleet_status()


@router.get("/api/drones/safe-count")
async def get_safe_drone_count(
    lat: float = Query(..., description="Latitude of operation zone"),
    lon: float = Query(..., description="Longitude of operation zone"),
    risk_score: float = Query(..., description="Risk score for the area (0-100)")
):
    """Calculate safe number of drones for deployment based on conditions"""
    return drone_fleet.calculate_safe_drone_count(
        weather={"wind": {"speed": 5}, "main": {"temp": 25}, "rain": {"1h": 0}, "visibility": 10000},
        risk_score=risk_score,
        location={"lat": lat, "lon": lon}
    )


@router.post("/api/drones/safe-count")
async def get_safe_drone_count_post(
    lat: float,
    lon: float,
    weather: Dict,
    risk_score: float
):
    """Calculate safe drone count with weather data"""
    return drone_fleet.calculate_safe_drone_count(
        weather=weather,
        risk_score=risk_score,
        location={"lat": lat, "lon": lon}
    )


@router.post("/api/drones/deploy")
async def deploy_drone(request: DroneDeployRequest):
    """Deploy a drone to a target location"""
    drone = next((d for d in drone_fleet.fleet_status if d["id"] == request.drone_id), None)
    
    if not drone:
        raise HTTPException(status_code=404, detail=f"Drone {request.drone_id} not found")
    
    if drone["status"] != "available":
        raise HTTPException(status_code=400, detail=f"Drone {request.drone_id} is not available")
    
    drone["status"] = "active"
    drone["location"] = {"lat": request.target_lat, "lon": request.target_lon}
    drone["altitude"] = request.altitude
    drone["speed"] = 15
    drone["last_update"] = datetime.now().isoformat()
    
    return {
        "status": "deployed",
        "drone_id": request.drone_id,
        "mission": {
            "type": request.mission_type,
            "target": {"lat": request.target_lat, "lon": request.target_lon},
            "altitude": request.altitude
        },
        "estimated_arrival": datetime.now().isoformat(),
        "timestamp": datetime.now().isoformat()
    }


@router.post("/api/drones/recall")
async def recall_drone(drone_id: str):
    """Recall a drone to base"""
    drone = next((d for d in drone_fleet.fleet_status if d["id"] == drone_id), None)
    
    if not drone:
        raise HTTPException(status_code=404, detail=f"Drone {drone_id} not found")
    
    drone["status"] = "returning"
    drone["speed"] = 20
    drone["last_update"] = datetime.now().isoformat()
    
    return {
        "status": "recall_initiated",
        "drone_id": drone_id,
        "estimated_return": datetime.now().isoformat(),
        "timestamp": datetime.now().isoformat()
    }


@router.post("/api/drones/position-estimate")
async def estimate_position(request: DronePositionEstimate):
    """Estimate drone position using satellite/weather data when GPS unavailable"""
    weather = request.weather_data or {}
    
    return drone_fleet.estimate_position_without_gps(
        lat=request.lat,
        lon=request.lon,
        weather=weather
    )


@router.get("/api/drones/types")
async def get_drone_types():
    """Get available drone types and their capabilities"""
    return {
        "drone_types": drone_fleet.DRONE_TYPES,
        "total_fleet_size": drone_fleet.TOTAL_DRONES,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/api/drones/{drone_id}")
async def get_drone_status(drone_id: str):
    """Get status of a specific drone"""
    drone = next((d for d in drone_fleet.fleet_status if d["id"] == drone_id), None)
    
    if not drone:
        raise HTTPException(status_code=404, detail=f"Drone {drone_id} not found")
    
    return drone


@router.post("/api/drones/charge")
async def charge_drone(drone_id: str):
    """Put a drone in charging mode"""
    drone = next((d for d in drone_fleet.fleet_status if d["id"] == drone_id), None)
    
    if not drone:
        raise HTTPException(status_code=404, detail=f"Drone {drone_id} not found")
    
    drone["status"] = "charging"
    drone["last_update"] = datetime.now().isoformat()
    
    return {
        "status": "charging",
        "drone_id": drone_id,
        "estimated_full_charge": datetime.now().isoformat(),
        "timestamp": datetime.now().isoformat()
    }

