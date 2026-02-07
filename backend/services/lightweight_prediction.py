"""
PRALAYA-NET Lightweight Prediction Engine
Risk scoring with rainfall, earthquake, and infrastructure weights
"""

import asyncio
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any
import random

class LightweightPredictionEngine:
    """Lightweight risk prediction with multiple factor weighting"""
    
    def __init__(self):
        self.data_dir = Path("backend/data/predictions")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Prediction weights (can be tuned)
        self.weights = {
            'rainfall': 0.35,      # 35% weight for rainfall data
            'earthquake': 0.30,    # 30% weight for earthquake data
            'infrastructure': 0.25, # 25% weight for infrastructure density
            'historical': 0.10       # 10% weight for historical patterns
        }
        
        # Risk thresholds
        self.thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8,
            'critical': 0.9
        }
        
        # Infrastructure density map (simplified)
        self.infrastructure_density = {
            'mumbai': 0.85,    # High density, critical infrastructure
            'delhi': 0.75,     # High density, good infrastructure
            'chennai': 0.65,   # Medium density, coastal vulnerability
            'kolkata': 0.70,    # Medium-high density
            'bangalore': 0.60,  # Medium density, modern infrastructure
            'hyderabad': 0.55,  # Medium density
            'pune': 0.50,       # Lower-medium density
            'jaipur': 0.45,     # Lower density
            'lucknow': 0.40,     # Low density
            'default': 0.50       # Default for unknown locations
        }
        
        # Historical disaster patterns (simplified)
        self.historical_patterns = {
            'flood': {
                'monsoon_risk': 0.7,      # High during monsoon (Jun-Sep)
                'cyclone_risk': 0.4,     # Medium during cyclone season
                'urban_impact': 0.8       # High impact in urban areas
            },
            'earthquake': {
                'seismic_zones': ['himalayan', 'northeast', 'gujarat'],
                'recurrence': 0.3,        # 30% chance in high-risk zones
                'building_vulnerability': 0.6  # Medium vulnerability
            },
            'cyclone': {
                'east_coast_risk': 0.6,   # High on east coast
                'west_coast_risk': 0.4,   # Medium on west coast
                'seasonal_pattern': 0.8     # Strong seasonal pattern
            }
        }
    
    def calculate_rainfall_risk(self, location: str = 'default', current_rainfall: float = 0) -> float:
        """Calculate rainfall risk factor"""
        # Get current month for seasonal adjustment
        current_month = datetime.datetime.now().month
        
        # Monsoon season (June-September) has higher risk
        if 6 <= current_month <= 9:
            seasonal_multiplier = 1.5
        else:
            seasonal_multiplier = 0.8
        
        # Base rainfall risk (0-1 scale)
        rainfall_risk = min(1.0, current_rainfall / 500)  # Normalize to 0-1 (500mm = 1.0)
        
        # Apply seasonal multiplier and location adjustment
        location_factor = self.infrastructure_density.get(location, self.infrastructure_density['default'])
        
        return rainfall_risk * seasonal_multiplier * location_factor
    
    def calculate_earthquake_risk(self, location: str = 'default', days_since_last: int = 365) -> float:
        """Calculate earthquake risk factor"""
        # Recent earthquake increases risk
        recency_factor = max(0.1, 1.0 - (days_since_last / 365))  # Decay over time
        
        # Location-based seismic risk
        if location in ['mumbai', 'pune', 'goa']:
            seismic_risk = 0.4  # Moderate seismic risk
        elif location in ['delhi', 'chandigarh']:
            seismic_risk = 0.3  # Lower seismic risk
        elif location in ['gujarat', 'rajasthan']:
            seismic_risk = 0.6  # Higher seismic risk
        else:
            seismic_risk = 0.5  # Default moderate risk
        
        return recency_factor * seismic_risk
    
    def calculate_infrastructure_risk(self, location: str = 'default') -> float:
        """Calculate infrastructure risk factor"""
        # Higher density = higher risk (more dependencies)
        density_risk = self.infrastructure_density.get(location, self.infrastructure_density['default'])
        
        # Age factor (simplified - older cities have higher risk)
        aging_cities = ['mumbai', 'kolkata', 'chennai']
        if location in aging_cities:
            age_factor = 1.2  # 20% higher risk for older infrastructure
        else:
            age_factor = 1.0
        
        return density_risk * age_factor
    
    def calculate_historical_risk(self, location: str = 'default', disaster_type: str = 'flood') -> float:
        """Calculate historical disaster risk factor"""
        patterns = self.historical_patterns.get(disaster_type, {})
        
        if not patterns:
            return 0.3  # Default low risk
        
        # Location-specific historical risk
        if location in ['mumbai', 'kolkata']:
            return patterns.get('urban_impact', 0.5)  # Higher urban impact
        elif location in ['chennai', 'visakhapatnam']:
            return patterns.get('east_coast_risk', 0.4)  # Coastal cyclone risk
        elif location in ['delhi', 'lucknow']:
            return patterns.get('monsoon_risk', 0.3)  # Monsoon flood risk
        else:
            return 0.3  # Default risk
    
    def calculate_combined_risk_score(self, location: str = 'default', 
                                current_rainfall: float = 0,
                                days_since_earthquake: int = 365,
                                recent_disasters: List[str] = None) -> Dict[str, Any]:
        """Calculate combined risk score using weighted factors"""
        
        # Calculate individual risk factors
        rainfall_risk = self.calculate_rainfall_risk(location, current_rainfall)
        earthquake_risk = self.calculate_earthquake_risk(location, days_since_earthquake)
        infrastructure_risk = self.calculate_infrastructure_risk(location)
        
        # Historical risk based on recent disasters
        if recent_disasters:
            # Higher risk if recent disasters occurred
            historical_risk = max([
                self.calculate_historical_risk(location, 'flood'),
                self.calculate_historical_risk(location, 'earthquake'),
                self.calculate_historical_risk(location, 'cyclone')
            ])
        else:
            historical_risk = 0.3  # Default historical risk
        
        # Weighted combination
        combined_risk = (
            rainfall_risk * self.weights['rainfall'] +
            earthquake_risk * self.weights['earthquake'] +
            infrastructure_risk * self.weights['infrastructure'] +
            historical_risk * self.weights['historical']
        )
        
        # Determine risk level
        if combined_risk >= self.thresholds['critical']:
            risk_level = 'critical'
        elif combined_risk >= self.thresholds['high']:
            risk_level = 'high'
        elif combined_risk >= self.thresholds['medium']:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        # Calculate confidence based on data availability
        confidence_factors = []
        if current_rainfall > 0:
            confidence_factors.append(0.8)  # Good confidence with rainfall data
        if days_since_earthquake < 365:
            confidence_factors.append(0.7)  # Moderate confidence with earthquake data
        if recent_disasters:
            confidence_factors.append(0.9)  # High confidence with historical data
        
        confidence = min(0.95, sum(confidence_factors) / len(confidence_factors)) if confidence_factors else 0.5
        
        return {
            'risk_score': round(combined_risk, 3),
            'risk_level': risk_level,
            'confidence': round(confidence, 2),
            'factors': {
                'rainfall_weight': round(rainfall_risk * self.weights['rainfall'], 3),
                'earthquake_weight': round(earthquake_risk * self.weights['earthquake'], 3),
                'infrastructure_weight': round(infrastructure_risk * self.weights['infrastructure'], 3),
                'historical_weight': round(historical_risk * self.weights['historical'], 3)
            },
            'individual_risks': {
                'rainfall_risk': round(rainfall_risk, 3),
                'earthquake_risk': round(earthquake_risk, 3),
                'infrastructure_risk': round(infrastructure_risk, 3),
                'historical_risk': round(historical_risk, 3)
            },
            'location': location,
            'weights_used': self.weights,
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def predict_regional_risk(self, regions: List[str] = None) -> Dict[str, Any]:
        """Predict risk for multiple regions"""
        if not regions:
            regions = ['mumbai', 'delhi', 'chennai', 'kolkata', 'bangalore']
        
        predictions = {}
        
        for region in regions:
            # Simulate current conditions for each region
            current_rainfall = random.uniform(0, 200)  # Current rainfall in mm
            days_since_earthquake = random.randint(30, 365)  # Days since last earthquake
            recent_disasters = random.choice([None, ['flood'], ['earthquake']])  # Recent disasters
            
            predictions[region] = self.calculate_combined_risk_score(
                location=region,
                current_rainfall=current_rainfall,
                days_since_earthquake=days_since_earthquake,
                recent_disasters=recent_disasters
            )
        
        return {
            'regional_predictions': predictions,
            'overall_risk': round(sum(p['risk_score'] for p in predictions.values()) / len(predictions), 3),
            'highest_risk_region': max(predictions.keys(), key=lambda k: predictions[k]['risk_score']),
            'lowest_risk_region': min(predictions.keys(), key=lambda k: predictions[k]['risk_score']),
            'timestamp': datetime.datetime.now().isoformat()
        }
    
    def save_prediction(self, prediction: Dict[str, Any], filename: str = None):
        """Save prediction to file"""
        if not filename:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"prediction_{timestamp}.json"
        
        try:
            filepath = self.data_dir / filename
            with open(filepath, 'w') as f:
                json.dump(prediction, f, indent=2)
            print(f"Saved prediction to: {filepath}")
        except Exception as e:
            print(f"Error saving prediction: {e}")
    
    def load_historical_data(self) -> Dict[str, Any]:
        """Load historical disaster data for pattern learning"""
        try:
            # Try to load combined events
            events_file = self.data_dir.parent / "disaster_history" / "combined_events.json"
            if events_file.exists():
                with open(events_file, 'r') as f:
                    events = json.load(f)
                    
                # Analyze patterns
                recent_events = events[-100:] if len(events) > 100 else events  # Last 100 events
                
                # Count by type and location
                event_patterns = {}
                location_patterns = {}
                
                for event in recent_events:
                    event_type = event.get('event_type', 'unknown')
                    location = self.extract_location_from_event(event)
                    
                    event_patterns[event_type] = event_patterns.get(event_type, 0) + 1
                    location_patterns[location] = location_patterns.get(location, 0) + 1
                
                return {
                    'total_events': len(recent_events),
                    'event_patterns': event_patterns,
                    'location_patterns': location_patterns,
                    'date_range': {
                        'earliest': min(e.get('timestamp', '') for e in recent_events),
                        'latest': max(e.get('timestamp', '') for e in recent_events)
                    },
                    'loaded_at': datetime.datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error loading historical data: {e}")
            return {}
    
    def extract_location_from_event(self, event: Dict[str, Any]) -> str:
        """Extract location from event data"""
        # Try to get location from event metadata
        metadata = event.get('metadata', {})
        if metadata and 'city' in metadata:
            return metadata['city'].lower()
        
        # Try to infer from coordinates (simplified)
        lat = event.get('latitude', 0)
        lon = event.get('longitude', 0)
        
        # Rough location inference based on coordinates
        if lat > 25 and lat < 30 and lon > 72 and lon < 78:
            return 'mumbai'
        elif lat > 27 and lat < 30 and lon > 76 and lon < 78:
            return 'delhi'
        elif lat > 12 and lat < 14 and lon > 79 and lon < 81:
            return 'chennai'
        elif lat > 22 and lat < 24 and lon > 87 and lon < 89:
            return 'kolkata'
        elif lat > 12 and lat < 14 and lon > 77 and lon < 78:
            return 'bangalore'
        
        return 'default'

# Global instance
lightweight_prediction_engine = LightweightPredictionEngine()

async def get_risk_prediction(location: str = None) -> Dict[str, Any]:
    """Get risk prediction for a location"""
    return lightweight_prediction_engine.calculate_combined_risk_score(location=location)

async def get_regional_risk_prediction(regions: List[str] = None) -> Dict[str, Any]:
    """Get regional risk predictions"""
    return lightweight_prediction_engine.predict_regional_risk(regions)

async def update_prediction_with_real_data(rainfall_mm: float = 0, 
                                       earthquake_magnitude: float = 0,
                                       location: str = 'default') -> Dict[str, Any]:
    """Update prediction with real-time data"""
    return lightweight_prediction_engine.calculate_combined_risk_score(
        location=location,
        current_rainfall=rainfall_mm,
        days_since_earthquake=365 if earthquake_magnitude == 0 else 30
    )
