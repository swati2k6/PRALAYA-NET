#!/usr/bin/env python3
"""
Disaster Injection Script - CLI tool to trigger disasters
"""

import requests
import sys
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:8000"

DISASTER_TYPES = ["flood", "fire", "earthquake", "cyclone", "landslide"]

def trigger_disaster(disaster_type, severity=0.7, location=None):
    """
    Trigger a disaster via API
    
    Args:
        disaster_type: Type of disaster
        severity: Severity score (0.0-1.0)
        location: Optional location dict
    """
    url = f"{API_BASE}/api/trigger/disaster"
    
    payload = {
        "disaster_type": disaster_type,
        "severity": severity,
        "location": location
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Disaster triggered: {disaster_type}")
        print(f"   Disaster ID: {result.get('disaster_id', 'N/A')}")
        print(f"   Location: {result.get('location', {}).get('name', 'N/A')}")
        print(f"   Alerts sent: {result.get('alerts_sent', {}).get('total', 0)}")
        
        return result
    except requests.exceptions.RequestException as e:
        print(f"❌ Error triggering disaster: {e}")
        return None

def clear_all():
    """Clear all disasters"""
    url = f"{API_BASE}/api/trigger/clear"
    
    try:
        response = requests.post(url, timeout=10)
        response.raise_for_status()
        print("✅ All disasters cleared")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error clearing disasters: {e}")
        return False

def get_status():
    """Get system status"""
    url = f"{API_BASE}/api/trigger/status"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        status = response.json()
        
        print("\n📊 System Status:")
        print(f"   Status: {status.get('status', 'N/A')}")
        print(f"   Active Disasters: {len(status.get('active_disasters', []))}")
        print(f"   Pending Alerts: {status.get('pending_alerts', 0)}")
        
        return status
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching status: {e}")
        return None

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("PRALAYA-NET Disaster Injection Tool")
        print("\nUsage:")
        print("  python inject_disaster.py <disaster_type> [severity]")
        print("  python inject_disaster.py status")
        print("  python inject_disaster.py clear")
        print(f"\nDisaster types: {', '.join(DISASTER_TYPES)}")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "status":
        get_status()
    elif command == "clear":
        clear_all()
    elif command in DISASTER_TYPES:
        severity = float(sys.argv[2]) if len(sys.argv) > 2 else 0.7
        trigger_disaster(command, severity)
    else:
        print(f"❌ Unknown command: {command}")
        print(f"Available commands: {', '.join(DISASTER_TYPES)}, status, clear")
        sys.exit(1)

if __name__ == "__main__":
    main()



