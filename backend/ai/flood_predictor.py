"""
Flood Predictor - LSTM model for time-series flood prediction
Simulated implementation for demo purposes
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
import random
from datetime import datetime, timedelta

class FloodPredictor:
    """
    LSTM-based flood prediction model
    Predicts flood risk based on historical weather data, precipitation, and river levels
    """
    
    def __init__(self):
        self.model_loaded = True
        self.prediction_horizon = 24  # hours
        self.feature_names = [
            "precipitation_24h",
            "precipitation_48h",
            "river_level",
            "soil_moisture",
            "temperature",
            "humidity"
        ]
    
    def predict_flood_risk(self, 
                          location: Dict,
                          weather_data: Dict,
                          historical_data: Optional[List[Dict]] = None) -> Dict:
        """
        Predict flood risk for a location
        
        Args:
            location: {"lat": float, "lon": float}
            weather_data: Current weather conditions
            historical_data: Historical weather data (optional)
        
        Returns:
            Flood risk prediction with probability and timeline
        """
        # Simulated LSTM prediction
        # In production, this would use actual LSTM model
        
        # Calculate risk factors
        precipitation = weather_data.get("precipitation", 0)
        humidity = weather_data.get("humidity", 50)
        temperature = weather_data.get("temperature", 25)
        
        # Risk calculation (simplified)
        risk_score = 0.0
        
        # Precipitation factor (0-0.5)
        if precipitation > 30:
            risk_score += 0.5
        elif precipitation > 15:
            risk_score += 0.3
        elif precipitation > 5:
            risk_score += 0.1
        
        # Humidity factor (0-0.2)
        if humidity > 80:
            risk_score += 0.2
        elif humidity > 60:
            risk_score += 0.1
        
        # Temperature factor (0-0.1)
        if temperature < 5:  # Freezing conditions
            risk_score += 0.1
        
        # Add some randomness for demo
        risk_score += random.uniform(-0.1, 0.2)
        risk_score = max(0.0, min(1.0, risk_score))
        
        # Predict timeline
        if risk_score > 0.6:
            time_to_flood = random.randint(2, 12)  # hours
        elif risk_score > 0.3:
            time_to_flood = random.randint(12, 48)  # hours
        else:
            time_to_flood = None
        
        return {
            "flood_risk": round(risk_score, 3),
            "risk_level": self._get_risk_level(risk_score),
            "time_to_flood_hours": time_to_flood,
            "prediction_horizon": self.prediction_horizon,
            "location": location,
            "factors": {
                "precipitation": precipitation,
                "humidity": humidity,
                "temperature": temperature
            },
            "predicted_at": datetime.now().isoformat(),
            "confidence": round(random.uniform(0.7, 0.95), 2)
        }
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Convert risk score to level"""
        if risk_score >= 0.8:
            return "critical"
        elif risk_score >= 0.6:
            return "high"
        elif risk_score >= 0.3:
            return "medium"
        else:
            return "low"
    
    def predict_multiple_locations(self, locations: List[Dict], weather_data: Dict) -> List[Dict]:
        """Predict flood risk for multiple locations"""
        predictions = []
        for location in locations:
            pred = self.predict_flood_risk(location, weather_data)
            predictions.append(pred)
        return predictions

# Global instance
flood_predictor = FloodPredictor()

