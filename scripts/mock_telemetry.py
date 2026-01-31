#!/usr/bin/env python3
"""
Mock Telemetry Generator - Generate fake drone telemetry data
"""

import requests
import time
import random
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"

def generate_telemetry(drone_id, base_lat=28.6139, base_lon=77.2090):
    """
    Generate mock telemetry data for a drone
    
    Args:
        drone_id: ID of the drone
        base_lat: Base latitude
        base_lon: Base longitude
    """
    telemetry = {
        "drone_id": drone_id,
        "location": {
            "lat": base_lat + random.uniform(-0.01, 0.01),
            "lon": base_lon + random.uniform(-0.01, 0.01)
        },
        "altitude": random.uniform(10, 120),
        "speed": random.uniform(5, 15),
        "heading": random.uniform(0, 360),
        "battery": max(0, random.uniform(50, 100)),
        "signal_strength": random.uniform(70, 100),
        "gps_status": "active" if random.random() > 0.1 else "degraded",
        "slam_status": "inactive",
        "camera_status": "active",
        "timestamp": datetime.now().isoformat()
    }
    
    return telemetry

def send_telemetry(drone_id, telemetry):
    """
    Send telemetry to backend (if endpoint exists)
    For now, just print it
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {drone_id}:")
    print(f"  Location: {telemetry['location']['lat']:.4f}, {telemetry['location']['lon']:.4f}")
    print(f"  Altitude: {telemetry['altitude']:.1f}m | Speed: {telemetry['speed']:.1f}m/s")
    print(f"  Battery: {telemetry['battery']:.1f}% | Signal: {telemetry['signal_strength']:.1f}%")
    print(f"  GPS: {telemetry['gps_status']} | SLAM: {telemetry['slam_status']}")
    print()

def main():
    """Main loop - generate telemetry continuously"""
    print("Mock Telemetry Generator")
    print("Generating telemetry for drone_1...")
    print("Press Ctrl+C to stop\n")
    
    drone_id = "drone_1"
    base_lat = 28.6139
    base_lon = 77.2090
    
    try:
        while True:
            telemetry = generate_telemetry(drone_id, base_lat, base_lon)
            send_telemetry(drone_id, telemetry)
            time.sleep(2)  # Update every 2 seconds
    except KeyboardInterrupt:
        print("\nStopped telemetry generation")

if __name__ == "__main__":
    main()



