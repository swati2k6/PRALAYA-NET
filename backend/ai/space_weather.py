"""
Space Weather - Solar storm and GPS failure detection
Simulates space weather events that can disrupt GPS and communication
"""

import random
from typing import Dict, Optional
from datetime import datetime, timedelta

class SpaceWeatherMonitor:
    """
    Monitors space weather events that can affect GPS and communication systems
    """
    
    def __init__(self):
        self.current_events = []
        self.gps_status = "operational"
        self.communication_status = "operational"
        self.solar_activity_level = 0.3  # Normal activity
        self.gps_failure_probability = 0.1  # 10% base chance of GPS issues
    
    def check_space_weather(self) -> Dict:
        """
        Check current space weather conditions
        Returns status of GPS and communication systems
        """
        # Simulate space weather events
        solar_activity = self.solar_activity_level
        
        # Occasionally trigger GPS issues
        if random.random() < self.gps_failure_probability:
            solar_activity = random.uniform(0.7, 1.0)
            self.solar_activity_level = solar_activity
        
        # Determine GPS status
        if solar_activity > 0.8:
            gps_status = "failed"
            gps_reliability = random.uniform(0.1, 0.3)
        elif solar_activity > 0.6:
            gps_status = "degraded"
            gps_reliability = random.uniform(0.4, 0.6)
        else:
            gps_status = "operational"
            gps_reliability = random.uniform(0.85, 1.0)
        
        # Determine communication status
        if solar_activity > 0.7:
            comm_status = "intermittent"
            comm_reliability = random.uniform(0.3, 0.6)
        else:
            comm_status = "operational"
            comm_reliability = random.uniform(0.8, 1.0)
        
        self.gps_status = gps_status
        self.communication_status = comm_status
        
        return {
            "gps_status": gps_status,
            "gps_reliability": round(gps_reliability, 2),
            "communication_status": comm_status,
            "communication_reliability": round(comm_reliability, 2),
            "solar_activity": round(solar_activity, 2),
            "solar_storm_active": solar_activity > 0.7,
            "timestamp": datetime.now().isoformat()
        }
    
    def simulate_solar_storm(self) -> Dict:
        """
        Simulate a solar storm event
        This would trigger V-SLAM mode for drones
        """
        storm_intensity = random.uniform(0.8, 1.0)
        duration_hours = random.randint(2, 12)
        
        self.solar_activity_level = storm_intensity
        
        event = {
            "type": "solar_storm",
            "intensity": round(storm_intensity, 2),
            "duration_hours": duration_hours,
            "gps_affected": True,
            "communication_affected": storm_intensity > 0.85,
            "start_time": datetime.now().isoformat(),
            "end_time": (datetime.now() + timedelta(hours=duration_hours)).isoformat()
        }
        
        self.current_events.append(event)
        
        # Update status
        self.gps_status = "failed"
        self.communication_status = "intermittent" if storm_intensity > 0.85 else "operational"
        
        return event
    
    def trigger_gps_failure(self):
        """Manually trigger GPS failure (for testing)"""
        self.solar_activity_level = 0.9
        self.gps_status = "failed"
        self.communication_status = "degraded"
    
    def is_gps_available(self) -> bool:
        """Check if GPS is currently available"""
        return self.gps_status == "operational"
    
    def should_use_slam(self) -> bool:
        """Determine if V-SLAM should be used (GPS unavailable)"""
        return not self.is_gps_available()
    
    def get_current_status(self) -> Dict:
        """Get current space weather status"""
        return {
            "gps_status": self.gps_status,
            "communication_status": self.communication_status,
            "active_events": len(self.current_events),
            "events": self.current_events[-5:] if self.current_events else [],
            "solar_activity": self.solar_activity_level,
            "timestamp": datetime.now().isoformat()
        }

# Global instance
space_weather_monitor = SpaceWeatherMonitor()
