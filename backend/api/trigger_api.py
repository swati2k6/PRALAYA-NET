"""
Trigger API - Inject disasters and trigger system response
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from orchestration.decision_engine import decision_engine
from orchestration.alert_manager import alert_manager
from api.satellite_api import satellite_zones
from config import DISASTER_TYPES, CRITICAL_INFRA
import random

router = APIRouter()

class DisasterTrigger(BaseModel):
    disaster_type: str
    severity: Optional[float] = 0.7
    location: Optional[Dict] = None
    metadata: Optional[Dict] = None

@router.post("/disaster")
async def trigger_disaster(trigger: DisasterTrigger):
    """
    Trigger a disaster scenario
    This simulates a disaster detection and triggers the full response pipeline
    """
    if trigger.disaster_type not in DISASTER_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid disaster type. Must be one of: {DISASTER_TYPES}"
        )
    
    # Generate location if not provided
    if not trigger.location:
        infra = random.choice(CRITICAL_INFRA)
        trigger.location = {
            "lat": infra["lat"],
            "lon": infra["lon"],
            "name": infra["name"]
        }
    
    # Run decision engine
    decision = decision_engine.process_disaster(
        disaster_type=trigger.disaster_type,
        severity=trigger.severity,
        location=trigger.location,
        metadata=trigger.metadata or {}
    )
    
    # Dispatch alerts
    alerts_sent = alert_manager.dispatch_alerts(decision["alerts"])
    
    return {
        "status": "disaster_triggered",
        "disaster_type": trigger.disaster_type,
        "location": trigger.location,
        "decision": decision,
        "alerts_sent": alerts_sent,
        "timestamp": decision.get("timestamp")
    }

@router.get("/status")
async def get_system_status():
    """Get current system status and active disasters"""
    # Get cascading analysis from decision engine
    cascading_analysis = None
    if decision_engine.decision_history:
        latest_decision = decision_engine.decision_history[-1]
        cascading_analysis = latest_decision.get("cascading_analysis")
    
    return {
        "status": "operational",
        "active_disasters": decision_engine.get_active_disasters(),
        "pending_alerts": alert_manager.get_pending_alerts_count(),
        "cascading_analysis": cascading_analysis,
        "system_health": {
            "ai_models": "operational",
            "orchestration": "operational",
            "hardware": "connected"
        }
    }

@router.post("/clear")
async def clear_all_disasters():
    """Clear all active disasters (for demo reset)"""
    decision_engine.clear_all()
    alert_manager.clear_all()
    # Clear satellite zones
    satellite_zones.clear()
    return {"status": "cleared", "message": "All disasters and alerts cleared"}
