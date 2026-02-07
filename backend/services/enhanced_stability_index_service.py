"""
Enhanced Stability Index Service
Dynamic computation with real-time updates every 10 seconds
"""

import asyncio
import uuid
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque

class StabilityLevel(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    HEALTHY = "healthy"
    EXCELLENT = "excellent"

class StabilityFactor(Enum):
    INFRASTRUCTURE_HEALTH = "infrastructure_health"
    CASCADE_RISK = "cascade_risk"
    AGENT_COORDINATION = "agent_coordination"
    RESOURCE_AVAILABILITY = "resource_availability"
    SYSTEM_PERFORMANCE = "system_performance"
    EXTERNAL_THREATS = "external_threats"

@dataclass
class StabilityMetric:
    metric_id: str
    factor: StabilityFactor
    value: float  # 0-1
    weight: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StabilityIndex:
    index_id: str
    overall_score: float  # 0-1
    level: StabilityLevel
    factors: Dict[str, float]
    trend: str  # improving, stable, declining
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class EnhancedStabilityIndexService:
    """Enhanced stability index service with dynamic computation and real-time updates"""
    
    def __init__(self):
        self.stability_history = deque(maxlen=1000)  # Keep last 1000 updates
        self.current_factors = {}
        self.update_interval = 10  # 10 seconds
        
    async def start_background_updates(self):
        """Start background stability index updates every 10 seconds"""
        print("🔄 Starting enhanced stability index background updates...")
        
        while True:
            try:
                # Calculate current stability index
                current_stability = await self.calculate_current_stability_index()
                
                # Store in history
                self.stability_history.append({
                    'timestamp': datetime.datetime.now(),
                    'stability_index': current_stability
                })
                
                # Broadcast to WebSocket clients
                await self.broadcast_stability_update(current_stability)
                
                print(f"✅ Stability index updated: {current_stability['overall_score']:.3f} ({current_stability['level']})")
                
                # Wait 10 seconds before next update
                await asyncio.sleep(self.update_interval)
                
            except asyncio.CancelledError:
                print("🛑 Enhanced stability index updates stopped")
                break
            except Exception as e:
                print(f"❌ Error in stability index update: {e}")
                await asyncio.sleep(self.update_interval)  # Continue trying even after errors
    
    async def calculate_current_stability_index(self) -> Dict[str, Any]:
        """Compute stability index dynamically using multiple factors"""
        try:
            # Get infrastructure health
            infrastructure_health = await self.get_infrastructure_health()
            
            # Get disaster risk score
            disaster_risk = await self.get_disaster_risk_score()
            
            # Get agent response capacity
            agent_response_capacity = await self.get_agent_response_capacity()
            
            # Calculate weighted stability index
            weights = {
                'infrastructure_health': 0.35,
                'disaster_risk': 0.30,
                'agent_response_capacity': 0.20,
                'temporal_stability': 0.15  # Historical stability trend
            }
            
            # Calculate individual factors
            infrastructure_factor = infrastructure_health.get('health_score', 0.7) * weights['infrastructure_health']
            disaster_factor = disaster_risk.get('risk_score', 0.3) * weights['disaster_risk']
            agent_factor = agent_response_capacity.get('capacity_score', 0.8) * weights['agent_response_capacity']
            
            # Temporal stability factor (based on recent trends)
            temporal_factor = await self.calculate_temporal_stability()
            
            # Combined stability score
            overall_score = min(1.0, (
                infrastructure_factor + 
                disaster_factor + 
                agent_factor + 
                temporal_factor
            ))
            
            # Determine stability level
            level = self.get_stability_level(overall_score)
            
            # Calculate individual factor scores
            factors = {
                'infrastructure_health': infrastructure_factor,
                'disaster_risk': disaster_factor,
                'agent_response_capacity': agent_factor,
                'temporal_stability': temporal_factor
            }
            
            # Add trend analysis
            trend = await self.calculate_stability_trend()
            
            stability_index = {
                'overall_score': overall_score,
                'level': level,
                'factors': factors,
                'trend': trend,
                'timestamp': datetime.datetime.now().isoformat(),
                'calculation_details': {
                    'weights': weights,
                    'raw_scores': {
                        'infrastructure_health': infrastructure_health.get('health_score', 0.7),
                        'disaster_risk': disaster_risk.get('risk_score', 0.3),
                        'agent_response_capacity': agent_response_capacity.get('capacity_score', 0.8),
                        'temporal_stability': temporal_factor
                    }
                }
            }
            
            return stability_index
            
        except Exception as e:
            print(f"Error calculating stability index: {e}")
            return {
                'overall_score': 0.5,
                'level': StabilityLevel.WARNING,
                'factors': {},
                'error': str(e)
            }
    
    async def get_infrastructure_health(self) -> Dict[str, Any]:
        """Get current infrastructure health status"""
        try:
            # Simulate infrastructure health monitoring
            health_score = random.uniform(0.6, 0.9)  # Current health level
            node_count = random.randint(45, 55)  # Number of monitored nodes
            operational_nodes = random.randint(40, 50)  # Nodes currently operational
            
            return {
                'health_score': health_score,
                'node_count': node_count,
                'operational_nodes': operational_nodes,
                'critical_nodes': node_count - operational_nodes,
                'last_maintenance': (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 7))).isoformat(),
                'system_uptime': round(random.uniform(0.85, 0.98), 3)
            }
            
        except Exception as e:
            print(f"Error getting infrastructure health: {e}")
            return {'health_score': 0.7, 'node_count': 50}
    
    async def get_disaster_risk_score(self) -> Dict[str, Any]:
        """Get current disaster risk score"""
        try:
            # Simulate disaster risk assessment
            active_threats = random.randint(0, 3)  # Current active threats
            risk_level = random.choice(['low', 'medium', 'high'])
            risk_score = {
                'low': 0.2,
                'medium': 0.4,
                'high': 0.7
            }.get(risk_level, 0.3)
            
            return {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'active_threats': active_threats,
                'threat_types': ['earthquake', 'flood', 'cyclone', 'wildfire'],
                'regional_risk': {
                    'north': random.uniform(0.1, 0.4),
                    'south': random.uniform(0.2, 0.6),
                    'east': random.uniform(0.15, 0.5),
                    'west': random.uniform(0.1, 0.3)
                }
            }
            
        except Exception as e:
            print(f"Error getting disaster risk score: {e}")
            return {'risk_score': 0.3, 'risk_level': 'medium'}
    
    async def get_agent_response_capacity(self) -> Dict[str, Any]:
        """Get current agent response capacity"""
        try:
            # Simulate agent network status
            total_agents = 12  # Total number of response agents
            active_agents = random.randint(8, 12)  # Currently active agents
            response_time = random.uniform(2.5, 8.0)  # Average response time in minutes
            success_rate = random.uniform(0.75, 0.95)  # Mission success rate
            
            # Calculate capacity score
            capacity_score = (active_agents / total_agents) * (success_rate * 0.7)
            
            return {
                'capacity_score': min(1.0, capacity_score),
                'total_agents': total_agents,
                'active_agents': active_agents,
                'response_time': response_time,
                'success_rate': success_rate,
                'current_missions': random.randint(1, 4)
            }
            
        except Exception as e:
            print(f"Error getting agent response capacity: {e}")
            return {'capacity_score': 0.8, 'total_agents': 12}
    
    async def calculate_temporal_stability(self) -> float:
        """Calculate temporal stability based on historical trends"""
        try:
            if len(self.stability_history) < 10:
                return 0.5  # Default value for insufficient history
            
            # Get last 24 hours of stability scores
            recent_scores = [entry['stability_index']['overall_score'] for entry in list(self.stability_history)[-24:]]
            
            if len(recent_scores) < 2:
                return 0.5
            
            # Calculate trend
            n = len(recent_scores)
            x = list(range(n))
            sum_x = sum(x)
            sum_y = sum(recent_scores)
            sum_xy = sum(x[i] * recent_scores[i] for i in range(n))
            sum_x2 = sum(x[i] ** 2 for i in range(n))
            
            if n * sum_x2 - sum_x ** 2 != 0:
                slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
                
                # Positive trend increases stability, negative trend decreases
                if abs(slope) < 0.01:
                    return 0.5  # Stable
                elif slope > 0.01:
                    return min(1.0, 0.5 + (slope * 2))  # Improving
                else:
                    return max(0.0, 0.5 - (abs(slope) * 2))  # Declining
            
            return 0.5
            
        except Exception as e:
            print(f"Error calculating temporal stability: {e}")
            return 0.5
    
    async def calculate_stability_trend(self) -> str:
        """Calculate stability trend over time"""
        try:
            if len(self.stability_history) < 5:
                return 'insufficient_data'
            
            # Get last 48 hours of data
            recent_entries = list(self.stability_history)[-48:]
            
            if len(recent_entries) < 2:
                return 'stable'
            
            # Simple linear regression to determine trend
            scores = [entry['stability_index']['overall_score'] for entry in recent_entries]
            n = len(scores)
            x = list(range(n))
            sum_x = sum(x)
            sum_y = sum(scores)
            sum_xy = sum(x[i] * scores[i] for i in range(n))
            sum_x2 = sum(x[i] ** 2 for i in range(n))
            
            if n * sum_x2 - sum_x ** 2 != 0:
                slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
                
                if abs(slope) < 0.01:
                    return 'stable'
                elif slope > 0.01:
                    return 'improving'
                else:
                    return 'declining'
            else:
                return 'stable'
                
        except Exception as e:
            print(f"Error calculating stability trend: {e}")
            return 'unknown'
    
    def get_stability_level(self, overall_score: float) -> StabilityLevel:
        """Determine stability level based on overall score"""
        if overall_score >= 0.8:
            return StabilityLevel.EXCELLENT
        elif overall_score >= 0.6:
            return StabilityLevel.HEALTHY
        elif overall_score >= 0.4:
            return StabilityLevel.WARNING
        else:
            return StabilityLevel.CRITICAL
    
    async def broadcast_stability_update(self, stability_index: Dict[str, Any]):
        """Broadcast stability update to WebSocket clients"""
        try:
            from websocket_manager import ws_manager
            
            message = {
                'type': 'stability_update',
                'stability_index': stability_index,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            await ws_manager.broadcast(message)
            print(f"📡 Broadcasted stability update: {stability_index['overall_score']:.3f}")
            
        except ImportError:
            print("WebSocket manager not available")
        except Exception as e:
            print(f"Error broadcasting stability update: {e}")

# Global instance
enhanced_stability_index_service = EnhancedStabilityIndexService()

# Background task for continuous updates
async def start_enhanced_stability_index_updates():
    """Start the enhanced stability index update service"""
    await enhanced_stability_index_service.start_background_updates()
