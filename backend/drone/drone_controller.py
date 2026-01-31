"""
Drone Controller - Manages drone fleet and commands
"""

from typing import Dict, List, Optional
import random
import math
from datetime import datetime, timedelta
from drone.slam_mode import slam_controller
from drone.telemetry import telemetry_gen
from config import DRONE_MAX_ALTITUDE
from ai.space_weather import space_weather_monitor

class DroneController:
    """
    Controls drone fleet operations with intelligent behavior
    """
    
    def __init__(self):
        self.drones = {}
        self.active_missions = {}
        self.telemetry_update_interval = 2.0  # seconds
    
    def deploy_drone(self, location: Dict) -> str:
        """
        Deploy a new drone to a location
        """
        drone_id = f"drone_{len(self.drones) + 1}_{datetime.now().strftime('%H%M%S')}"
        
        # Check if GPS is available
        gps_available = space_weather_monitor.is_gps_available()
        slam_required = not gps_available
        
        self.drones[drone_id] = {
            "id": drone_id,
            "status": "deployed",
            "location": location.copy(),
            "altitude": 0,
            "battery": 100.0,
            "slam_enabled": slam_required,
            "gps_available": gps_available,
            "mission": "standby",
            "deployed_at": datetime.now().isoformat(),
            "last_update": datetime.now().isoformat(),
            "velocity": {
                "lat": 0.0,
                "lon": 0.0,
                "altitude": 0.0
            }
        }
        
        # Initialize telemetry
        telemetry_gen.telemetry_data[drone_id] = {
            "drone_id": drone_id,
            "location": location.copy(),
            "altitude": 0,
            "speed": 0,
            "heading": 0,
            "battery": 100.0,
            "signal_strength": 95.0,
            "gps_status": "active" if gps_available else "failed",
            "slam_status": "active" if slam_required else "inactive",
            "camera_status": "active",
            "timestamp": datetime.now().isoformat()
        }
        
        # Enable SLAM if needed
        if slam_required:
            slam_controller.enable_slam(drone_id)
            telemetry_gen.set_gps_status(drone_id, "failed")
            telemetry_gen.set_slam_status(drone_id, "active")
        
        return drone_id
    
    def execute_command(self, drone_id: str, action: str, params: Dict = None) -> Optional[Dict]:
        """
        Execute a command on a drone
        """
        if drone_id not in self.drones:
            return None
        
        drone = self.drones[drone_id]
        params = params or {}
        
        if action == "takeoff":
            drone["status"] = "flying"
            drone["altitude"] = params.get("altitude", 50)
            drone["mission"] = params.get("mission", "reconnaissance")
            
            # Update telemetry
            if drone_id in telemetry_gen.telemetry_data:
                telemetry_gen.telemetry_data[drone_id]["altitude"] = drone["altitude"]
                telemetry_gen.telemetry_data[drone_id]["status"] = "flying"
        
        elif action == "land":
            drone["status"] = "landed"
            drone["altitude"] = 0
            drone["mission"] = "standby"
            
            if drone_id in telemetry_gen.telemetry_data:
                telemetry_gen.telemetry_data[drone_id]["altitude"] = 0
                telemetry_gen.telemetry_data[drone_id]["status"] = "landed"
        
        elif action == "move":
            target_lat = params.get("lat", drone["location"]["lat"])
            target_lon = params.get("lon", drone["location"]["lon"])
            
            # Calculate heading and velocity
            lat_diff = target_lat - drone["location"]["lat"]
            lon_diff = target_lon - drone["location"]["lon"]
            
            distance = math.sqrt(lat_diff**2 + lon_diff**2)
            heading = math.degrees(math.atan2(lon_diff, lat_diff))
            if heading < 0:
                heading += 360
            
            # Simulate movement (gradual update)
            drone["location"]["lat"] += lat_diff * 0.1
            drone["location"]["lon"] += lon_diff * 0.1
            
            drone["velocity"]["lat"] = lat_diff * 0.001  # m/s equivalent
            drone["velocity"]["lon"] = lon_diff * 0.001
            
            if drone_id in telemetry_gen.telemetry_data:
                telemetry_gen.telemetry_data[drone_id]["location"]["lat"] = drone["location"]["lat"]
                telemetry_gen.telemetry_data[drone_id]["location"]["lon"] = drone["location"]["lon"]
                telemetry_gen.telemetry_data[drone_id]["heading"] = heading
                telemetry_gen.telemetry_data[drone_id]["speed"] = min(distance * 1000, 15)  # m/s
        
        elif action == "slam_enable":
            drone["slam_enabled"] = True
            slam_controller.enable_slam(drone_id)
            telemetry_gen.set_slam_status(drone_id, "active")
            telemetry_gen.set_gps_status(drone_id, "failed")
        
        elif action == "slam_disable":
            drone["slam_enabled"] = False
            slam_controller.disable_slam(drone_id)
            if space_weather_monitor.is_gps_available():
                telemetry_gen.set_slam_status(drone_id, "inactive")
                telemetry_gen.set_gps_status(drone_id, "active")
        
        drone["last_update"] = datetime.now().isoformat()
        
        return {
            "status": "success",
            "drone_id": drone_id,
            "action": action,
            "drone_status": drone["status"],
            "timestamp": datetime.now().isoformat()
        }
    
    def update_drone_positions(self):
        """Update all active drones' positions (called periodically)"""
        for drone_id, drone in self.drones.items():
            if drone["status"] == "flying":
                # Simulate movement if on mission
                if drone["mission"] != "standby":
                    # Add small random movement
                    drone["location"]["lat"] += random.uniform(-0.0001, 0.0001)
                    drone["location"]["lon"] += random.uniform(-0.0001, 0.0001)
                    
                    # Update battery drain
                    drone["battery"] = max(0, drone["battery"] - 0.05)
                    
                    # Update telemetry
                    if drone_id in telemetry_gen.telemetry_data:
                        telemetry = telemetry_gen.telemetry_data[drone_id]
                        telemetry["location"] = drone["location"].copy()
                        telemetry["battery"] = drone["battery"]
                        telemetry["altitude"] = drone["altitude"]
                        telemetry["timestamp"] = datetime.now().isoformat()
                        
                        # Update SLAM map points if SLAM is active
                        if drone["slam_enabled"]:
                            slam_controller.add_map_point(drone_id, {
                                "x": drone["location"]["lat"],
                                "y": drone["location"]["lon"],
                                "z": drone["altitude"],
                                "descriptor": [random.uniform(0, 1) for _ in range(64)]
                            })
                
                drone["last_update"] = datetime.now().isoformat()
    
    def get_drone(self, drone_id: str) -> Optional[Dict]:
        """Get drone status"""
        if drone_id in self.drones:
            return self.drones[drone_id].copy()
        return None
    
    def get_all_drones(self) -> List[Dict]:
        """Get all drones with current status"""
        # Update positions before returning
        self.update_drone_positions()
        return [d.copy() for d in self.drones.values()]
    
    def get_slam_status(self, drone_id: str) -> Optional[Dict]:
        """Get V-SLAM status for a drone"""
        if drone_id not in self.drones:
            return None
        
        drone = self.drones[drone_id]
        slam_status = slam_controller.get_status(drone_id)
        
        return {
            "drone_id": drone_id,
            "slam_enabled": drone.get("slam_enabled", False),
            "gps_available": drone.get("gps_available", True),
            "slam_status": slam_status,
            "navigation_mode": "V-SLAM" if drone.get("slam_enabled") else "GPS"
        }
    
    def enable_slam(self, drone_id: str) -> bool:
        """Enable V-SLAM for a drone"""
        if drone_id not in self.drones:
            return False
        
        self.execute_command(drone_id, "slam_enable")
        return True
    
    def disable_slam(self, drone_id: str) -> bool:
        """Disable V-SLAM for a drone"""
        if drone_id not in self.drones:
            return False
        
        self.execute_command(drone_id, "slam_disable")
        return True

# Global instance
drone_controller = DroneController()
