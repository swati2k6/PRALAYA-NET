"""
Alerts API - Endpoint for ESP32 to poll alerts
"""

from fastapi import APIRouter
from orchestration.alert_manager import alert_manager

router = APIRouter()

@router.get("/esp32")
async def get_esp32_alerts():
    """
    Get alerts formatted for ESP32
    ESP32 polls this endpoint periodically
    """
    alerts = alert_manager.get_esp32_alerts()
    return {
        "alerts": alerts,
        "count": len(alerts),
        "timestamp": alert_manager.pending_alerts[-1]["timestamp"] if alert_manager.pending_alerts else None
    }

@router.get("/dashboard")
async def get_dashboard_alerts():
    """
    Get alerts for dashboard
    """
    alerts = alert_manager.get_pending_alerts("dashboard")
    return {
        "alerts": alerts,
        "count": len(alerts)
    }



