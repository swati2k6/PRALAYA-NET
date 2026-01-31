"""
Alert Manager - Sends alerts to React Dashboard and ESP32
"""

from typing import List, Dict, Optional
from datetime import datetime
import requests
from config import ESP32_BASE_URL

class AlertManager:
    """
    Manages alert distribution to multiple channels:
    - Dashboard (via polling)
    - ESP32 (via HTTP polling)
    - Mobile (future)
    """
    
    def __init__(self):
        self.pending_alerts = []
        self.sent_alerts = []
        self.alert_history = []
        self.esp32_connected = False
    
    def dispatch_alerts(self, alerts: List[Dict]) -> Dict:
        """
        Dispatch alerts to all channels
        """
        results = {
            "total": len(alerts),
            "dashboard": 0,
            "esp32": 0,
            "failed": 0,
            "alert_ids": []
        }
        
        for alert in alerts:
            alert["id"] = alert.get("id", f"alert_{len(self.pending_alerts) + 1}")
            alert["created_at"] = datetime.now().isoformat()
            alert["status"] = "pending"
            
            # Add to pending queue (dashboard will poll)
            self.pending_alerts.append(alert)
            results["dashboard"] += 1
            results["alert_ids"].append(alert["id"])
            
            # Format for ESP32
            esp32_alert = self._format_for_esp32(alert)
            if esp32_alert:
                results["esp32"] += 1
            
            # Add to history
            self.alert_history.append({
                **alert,
                "dispatched_at": datetime.now().isoformat()
            })
        
        return results
    
    def _format_for_esp32(self, alert: Dict) -> Optional[Dict]:
        """Format alert for ESP32 display"""
        message = alert.get("message", "")
        
        # Truncate for LCD (16 characters typical)
        if len(message) > 16:
            message = message[:13] + "..."
        
        return {
            "id": alert.get("id"),
            "type": alert.get("type", "alert"),
            "severity": alert.get("severity", 0.5),
            "message": message,
            "timestamp": alert.get("timestamp", alert.get("created_at"))
        }
    
    def get_pending_alerts(self, channel: str = "dashboard") -> List[Dict]:
        """
        Get pending alerts for a channel
        Called by dashboard or ESP32 when polling
        """
        alerts = [
            a for a in self.pending_alerts 
            if a.get("channel") == channel or channel == "dashboard" or not a.get("channel")
        ]
        
        return alerts
    
    def clear_delivered_alerts(self, alert_ids: List[str]):
        """Clear alerts that have been delivered"""
        self.pending_alerts = [
            a for a in self.pending_alerts 
            if a.get("id") not in alert_ids
        ]
    
    def get_pending_alerts_count(self) -> int:
        """Get count of pending alerts"""
        return len(self.pending_alerts)
    
    def get_esp32_alerts(self) -> List[Dict]:
        """
        Get alerts formatted for ESP32
        ESP32 polls this endpoint
        """
        alerts = self.get_pending_alerts("esp32")
        
        # Format for ESP32 (simplified message)
        formatted = []
        for alert in alerts:
            formatted.append(self._format_for_esp32(alert))
        
        return formatted
    
    def get_alert_history(self, limit: int = 50) -> List[Dict]:
        """Get recent alert history"""
        return self.alert_history[-limit:]
    
    def clear_all(self):
        """Clear all alerts"""
        self.pending_alerts.clear()
        self.sent_alerts.clear()

# Global instance
alert_manager = AlertManager()
