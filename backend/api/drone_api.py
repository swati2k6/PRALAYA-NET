"""
Drone API - Control and monitor drones
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Optional
from drone.drone_controller import drone_controller
from drone.telemetry import telemetry_gen
from pydantic import BaseModel
import asyncio

router = APIRouter()

class DroneCommand(BaseModel):
    action: str  # "takeoff", "land", "move", "slam_enable", "slam_disable"
    params: Optional[Dict] = None

@router.get("/status")
async def get_drone_status():
    """
    Get status of all drones
    """
    drones = drone_controller.get_all_drones()
    return {
        "drones": drones,
        "count": len(drones),
        "active": len([d for d in drones if d.get("status") == "active"])
    }

@router.get("/status/{drone_id}")
async def get_drone_status_by_id(drone_id: str):
    """Get status of a specific drone"""
    drone = drone_controller.get_drone(drone_id)
    if not drone:
        raise HTTPException(status_code=404, detail=f"Drone {drone_id} not found")
    return drone

@router.get("/telemetry/{drone_id}")
async def get_drone_telemetry(drone_id: str):
    """Get real-time telemetry for a drone"""
    telemetry = telemetry_gen.get_telemetry(drone_id)
    if not telemetry:
        raise HTTPException(status_code=404, detail=f"Telemetry for {drone_id} not found")
    return telemetry

@router.post("/command/{drone_id}")
async def send_drone_command(drone_id: str, command: DroneCommand):
    """Send a command to a drone"""
    result = drone_controller.execute_command(drone_id, command.action, command.params or {})
    if not result:
        raise HTTPException(status_code=400, detail=f"Failed to execute command: {command.action}")
    return result

@router.post("/deploy")
async def deploy_drone(location: Dict):
    """
    Deploy a new drone to a location
    """
    drone_id = drone_controller.deploy_drone(location)
    return {
        "status": "deployed",
        "drone_id": drone_id,
        "location": location
    }

@router.get("/slam/{drone_id}")
async def get_slam_status(drone_id: str):
    """Get V-SLAM status for a drone"""
    slam_status = drone_controller.get_slam_status(drone_id)
    if slam_status is None:
        raise HTTPException(status_code=404, detail=f"Drone {drone_id} not found")
    return slam_status

@router.post("/slam/{drone_id}/enable")
async def enable_slam(drone_id: str):
    """Enable V-SLAM for a drone"""
    result = drone_controller.enable_slam(drone_id)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to enable SLAM")
    return {"status": "slam_enabled", "drone_id": drone_id}

@router.post("/slam/{drone_id}/disable")
async def disable_slam(drone_id: str):
    """Disable V-SLAM for a drone"""
    result = drone_controller.disable_slam(drone_id)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to disable SLAM")
    return {"status": "slam_disabled", "drone_id": drone_id}

