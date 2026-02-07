"""
Digital Twin Cascade Forecast Engine
Real dependency graph-based cascade prediction and pre-stabilization
"""

import asyncio
import uuid
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import numpy as np
from collections import defaultdict, deque

class NodeType(Enum):
    POWER_GRID = "power_grid"
    TELECOM_TOWER = "telecom_tower"
    WATER_SYSTEM = "water_system"
    TRANSPORT_BRIDGE = "transport_bridge"
    HOSPITAL = "hospital"
    SCHOOL = "school"
    COMMUNICATION_CENTER = "communication_center"

class FailureMode(Enum):
    OVERLOAD = "overload"
    WEATHER_DAMAGE = "weather_damage"
    STRUCTURAL_DAMAGE = "structural_damage"
    EQUIPMENT_FAILURE = "equipment_failure"
    POWER_OUTAGE = "power_outage"
    CONNECTIVITY_LOSS = "connectivity_loss"

class CascadeSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class DependencyEdge:
    """Infrastructure dependency relationship"""
    source_node: str
    target_node: str
    dependency_type: str
    failure_propagation_weight: float  # 0-1, how likely failure propagates
    recovery_dependency: float  # 0-1, how much target depends on source for recovery
    distance_km: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_node": self.source_node,
            "target_node": self.target_node,
            "dependency_type": self.dependency_type,
            "failure_propagation_weight": self.failure_propagation_weight,
            "recovery_dependency": self.recovery_dependency,
            "distance_km": self.distance_km
        }

@dataclass
class InfrastructureNode:
    """Infrastructure node in dependency graph"""
    node_id: str
    name: str
    node_type: NodeType
    location: Dict[str, float]  # lat, lon
    capacity: float
    current_load: float
    health_score: float  # 0-1
    redundancy_level: int  # 0-5, number of backup systems
    repair_time_hours: float
    criticality_score: float  # 0-1, importance to overall system
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "node_type": self.node_type.value,
            "location": self.location,
            "capacity": self.capacity,
            "current_load": self.current_load,
            "health_score": self.health_score,
            "redundancy_level": self.redundancy_level,
            "repair_time_hours": self.repair_time_hours,
            "criticality_score": self.criticality_score,
            "dependencies": self.dependencies,
            "dependents": self.dependents
        }

@dataclass
class CascadePrediction:
    """Cascade failure prediction"""
    prediction_id: str
    timestamp: datetime
    initial_failure_node: str
    failure_mode: FailureMode
    cascade_probability: float
    predicted_radius_km: float
    affected_nodes: List[str]
    cascade_timeline: List[Dict[str, Any]]
    total_impact_score: float
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "prediction_id": self.prediction_id,
            "timestamp": self.timestamp.isoformat(),
            "initial_failure_node": self.initial_failure_node,
            "failure_mode": self.failure_mode.value,
            "cascade_probability": self.cascade_probability,
            "predicted_radius_km": self.predicted_radius_km,
            "affected_nodes": self.affected_nodes,
            "cascade_timeline": self.cascade_timeline,
            "total_impact_score": self.total_impact_score,
            "confidence": self.confidence
        }

@dataclass
class PreStabilizationStrategy:
    """Pre-emptive stabilization strategy"""
    strategy_id: str
    target_nodes: List[str]
    stabilization_actions: List[Dict[str, Any]]
    expected_cascade_reduction: float
    implementation_cost: float
    implementation_time_minutes: int
    priority_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy_id": self.strategy_id,
            "target_nodes": self.target_nodes,
            "stabilization_actions": self.stabilization_actions,
            "expected_cascade_reduction": self.expected_cascade_reduction,
            "implementation_cost": self.implementation_cost,
            "implementation_time_minutes": self.implementation_time_minutes,
            "priority_score": self.priority_score
        }

@dataclass
class CriticalNodeAnalysis:
    """Critical node analysis for pre-stabilization"""
    node_id: str
    centrality_score: float
    cascade_contribution_score: float
    vulnerability_score: float
    stabilization_priority: float
    recommended_actions: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "centrality_score": self.centrality_score,
            "cascade_contribution_score": self.cascade_contribution_score,
            "vulnerability_score": self.vulnerability_score,
            "stabilization_priority": self.stabilization_priority,
            "recommended_actions": self.recommended_actions
        }

class DigitalTwinCascadeForecastEngine:
    """Real-time cascade prediction and pre-stabilization engine"""
    
    def __init__(self):
        self.nodes: Dict[str, InfrastructureNode] = {}
        self.edges: Dict[str, DependencyEdge] = {}
        self.dependency_graph: Dict[str, List[str]] = defaultdict(list)
        self.reverse_dependency_graph: Dict[str, List[str]] = defaultdict(list)
        self.cascade_predictions: List[CascadePrediction] = []
        self.critical_node_analyses: Dict[str, CriticalNodeAnalysis] = {}
        self.pre_stabilization_strategies: Dict[str, PreStabilizationStrategy] = {}
        
        # Initialize infrastructure network
        self._initialize_infrastructure_network()
        
        # Start continuous monitoring
        asyncio.create_task(self._continuous_monitoring())
    
    def _initialize_infrastructure_network(self):
        """Initialize realistic infrastructure dependency network"""
        
        # Create infrastructure nodes
        node_configs = [
            # Power infrastructure
            {"id": "power_main_mumbai", "name": "Mumbai Main Power Station", "type": NodeType.POWER_GRID, "lat": 19.0760, "lon": 72.8777, "capacity": 1000, "criticality": 0.95},
            {"id": "power_suburban_1", "name": "Suburban Power Substation 1", "type": NodeType.POWER_GRID, "lat": 19.1160, "lon": 72.9177, "capacity": 500, "criticality": 0.8},
            {"id": "power_suburban_2", "name": "Suburban Power Substation 2", "type": NodeType.POWER_GRID, "lat": 19.0360, "lon": 72.8377, "capacity": 500, "criticality": 0.8},
            {"id": "power_industrial", "name": "Industrial Power Plant", "type": NodeType.POWER_GRID, "lat": 19.1560, "lon": 72.9577, "capacity": 800, "criticality": 0.85},
            
            # Telecom infrastructure
            {"id": "telecom_main_mumbai", "name": "Mumbai Main Telecom Tower", "type": NodeType.TELECOM_TOWER, "lat": 19.0860, "lon": 72.8877, "capacity": 100, "criticality": 0.9},
            {"id": "telecom_south", "name": "South Mumbai Tower", "type": NodeType.TELECOM_TOWER, "lat": 19.0260, "lon": 72.8277, "capacity": 80, "criticality": 0.7},
            {"id": "telecom_north", "name": "North Mumbai Tower", "type": NodeType.TELECOM_TOWER, "lat": 19.1460, "lon": 72.9477, "capacity": 80, "criticality": 0.7},
            {"id": "telecom_west", "name": "West Mumbai Tower", "type": NodeType.TELECOM_TOWER, "lat": 19.0760, "lon": 72.8177, "capacity": 60, "criticality": 0.6},
            
            # Water infrastructure
            {"id": "water_main_mumbai", "name": "Mumbai Main Water Plant", "type": NodeType.WATER_SYSTEM, "lat": 19.0560, "lon": 72.8577, "capacity": 2000, "criticality": 0.9},
            {"id": "water_east", "name": "East Water Treatment", "type": NodeType.WATER_SYSTEM, "lat": 19.1260, "lon": 72.9277, "capacity": 800, "criticality": 0.75},
            {"id": "water_west", "name": "West Water Treatment", "type": NodeType.WATER_SYSTEM, "lat": 19.0060, "lon": 72.7877, "capacity": 800, "criticality": 0.75},
            
            # Transport infrastructure
            {"id": "bridge_sealink", "name": "Sea Link Bridge", "type": NodeType.TRANSPORT_BRIDGE, "lat": 19.0160, "lon": 72.8177, "capacity": 500, "criticality": 0.85},
            {"id": "bridge_eastern", "name": "Eastern Express Bridge", "type": NodeType.TRANSPORT_BRIDGE, "lat": 19.1060, "lon": 72.9077, "capacity": 300, "criticality": 0.7},
            
            # Healthcare infrastructure
            {"id": "hospital_main", "name": "Mumbai Main Hospital", "type": NodeType.HOSPITAL, "lat": 19.1360, "lon": 72.9377, "capacity": 1000, "criticality": 0.95},
            {"id": "hospital_south", "name": "South Mumbai Hospital", "type": NodeType.HOSPITAL, "lat": 19.0060, "lon": 72.8077, "capacity": 500, "criticality": 0.8},
            {"id": "hospital_north", "name": "North Mumbai Hospital", "type": NodeType.HOSPITAL, "lat": 19.1660, "lon": 72.9677, "capacity": 500, "criticality": 0.8},
            
            # Communication centers
            {"id": "comm_control", "name": "Communication Control Center", "type": NodeType.COMMUNICATION_CENTER, "lat": 19.0760, "lon": 72.8777, "capacity": 200, "criticality": 0.98},
            {"id": "comm_backup", "name": "Backup Communication Center", "type": NodeType.COMMUNICATION_CENTER, "lat": 19.1460, "lon": 72.9477, "capacity": 100, "criticality": 0.85}
        ]
        
        # Create nodes
        for config in node_configs:
            node = InfrastructureNode(
                node_id=config["id"],
                name=config["name"],
                node_type=config["type"],
                location={"lat": config["lat"], "lon": config["lon"]},
                capacity=config["capacity"],
                current_load=np.random.uniform(0.3, 0.9) * config["capacity"],
                health_score=np.random.uniform(0.7, 1.0),
                redundancy_level=np.random.randint(1, 4),
                repair_time_hours=np.random.uniform(2, 24),
                criticality_score=config["criticality"]
            )
            self.nodes[node.node_id] = node
        
        # Create realistic dependencies
        dependencies = [
            # Power dependencies
            ("power_main_mumbai", "telecom_main_mumbai", "power_supply", 0.9, 0.8, 5.0),
            ("power_main_mumbai", "water_main_mumbai", "power_supply", 0.85, 0.9, 8.0),
            ("power_main_mumbai", "hospital_main", "power_supply", 0.95, 0.9, 3.0),
            ("power_main_mumbai", "comm_control", "power_supply", 0.98, 0.95, 2.0),
            ("power_suburban_1", "telecom_south", "power_supply", 0.8, 0.7, 3.0),
            ("power_suburban_2", "telecom_north", "power_supply", 0.8, 0.7, 3.0),
            ("power_industrial", "bridge_sealink", "power_supply", 0.7, 0.6, 10.0),
            
            # Telecom dependencies
            ("telecom_main_mumbai", "comm_control", "data_link", 0.9, 0.8, 1.0),
            ("telecom_south", "hospital_south", "emergency_comm", 0.7, 0.6, 2.0),
            ("telecom_north", "hospital_north", "emergency_comm", 0.7, 0.6, 2.0),
            
            # Water dependencies
            ("water_main_mumbai", "hospital_main", "water_supply", 0.9, 0.8, 2.0),
            ("water_main_mumbai", "power_main_mumbai", "cooling_water", 0.6, 0.5, 5.0),
            ("water_east", "hospital_south", "water_supply", 0.8, 0.7, 1.0),
            ("water_west", "hospital_north", "water_supply", 0.8, 0.7, 1.0),
            
            # Transport dependencies
            ("bridge_sealink", "hospital_main", "patient_transport", 0.6, 0.5, 8.0),
            ("bridge_eastern", "hospital_south", "patient_transport", 0.5, 0.4, 5.0),
            
            # Communication dependencies
            ("comm_control", "power_main_mumbai", "control_signals", 0.8, 0.7, 2.0),
            ("comm_backup", "comm_control", "backup_link", 0.9, 0.8, 15.0),
            
            # Cross-dependencies
            ("telecom_main_mumbai", "power_suburban_1", "coordination", 0.3, 0.2, 7.0),
            ("hospital_main", "telecom_main_mumbai", "medical_coordination", 0.4, 0.3, 1.0),
            ("water_main_mumbai", "telecom_main_mumbai", "sensor_data", 0.2, 0.1, 3.0)
        ]
        
        # Create dependency edges
        for source, target, dep_type, prop_weight, rec_dep, distance in dependencies:
            edge_id = f"{source}_{target}"
            edge = DependencyEdge(
                source_node=source,
                target_node=target,
                dependency_type=dep_type,
                failure_propagation_weight=prop_weight,
                recovery_dependency=rec_dep,
                distance_km=distance
            )
            self.edges[edge_id] = edge
            
            # Update dependency graphs
            self.dependency_graph[source].append(target)
            self.reverse_dependency_graph[target].append(source)
            
            # Update node dependencies
            self.nodes[source].dependents.append(target)
            self.nodes[target].dependencies.append(source)
        
        # Calculate critical node analyses
        self._calculate_critical_node_analyses()
    
    def _calculate_critical_node_analyses(self):
        """Calculate critical node analyses for all nodes"""
        for node_id, node in self.nodes.items():
            # Calculate centrality score (number of connections weighted by criticality)
            centrality_score = 0
            for dependent_id in node.dependents:
                centrality_score += self.nodes[dependent_id].criticality_score * 0.5
            for dependency_id in node.dependencies:
                centrality_score += self.nodes[dependency_id].criticality_score * 0.3
            
            # Normalize centrality score
            max_centrality = max(len(node.dependents) + len(node.dependencies), 1)
            centrality_score = min(1.0, centrality_score / max_centrality)
            
            # Calculate cascade contribution score
            cascade_contribution_score = self._calculate_cascade_contribution(node_id)
            
            # Calculate vulnerability score
            vulnerability_score = (1 - node.health_score) * (1 - node.redundancy_level / 5) * node.criticality_score
            
            # Calculate stabilization priority
            stabilization_priority = (centrality_score * 0.4 + 
                                   cascade_contribution_score * 0.4 + 
                                   vulnerability_score * 0.2)
            
            # Generate recommended actions
            recommended_actions = []
            if vulnerability_score > 0.7:
                recommended_actions.append("increase_redundancy")
            if centrality_score > 0.8:
                recommended_actions.append("enhance_monitoring")
            if cascade_contribution_score > 0.7:
                recommended_actions.append("pre_stabilization")
            
            analysis = CriticalNodeAnalysis(
                node_id=node_id,
                centrality_score=centrality_score,
                cascade_contribution_score=cascade_contribution_score,
                vulnerability_score=vulnerability_score,
                stabilization_priority=stabilization_priority,
                recommended_actions=recommended_actions
            )
            
            self.critical_node_analyses[node_id] = analysis
    
    def _calculate_cascade_contribution(self, node_id: str) -> float:
        """Calculate how much a node contributes to cascades"""
        total_contribution = 0
        visited = set()
        
        def dfs_contribution(current_node: str, depth: int) -> float:
            if current_node in visited or depth > 5:
                return 0
            
            visited.add(current_node)
            contribution = 0
            
            for dependent_id in self.nodes[current_node].dependents:
                edge_id = f"{current_node}_{dependent_id}"
                if edge_id in self.edges:
                    edge = self.edges[edge_id]
                    weight = edge.failure_propagation_weight
                    contribution += weight * (1 - depth * 0.1)  # Decrease with depth
                    contribution += dfs_contribution(dependent_id, depth + 1) * weight * 0.5
            
            return contribution
        
        return min(1.0, dfs_contribution(node_id, 0) / 10)
    
    async def _continuous_monitoring(self):
        """Continuous monitoring for cascade risks"""
        while True:
            try:
                # Update node health scores (simulate degradation)
                for node in self.nodes.values():
                    node.health_score *= np.random.uniform(0.98, 1.0)
                    node.current_load = np.random.uniform(0.3, 0.9) * node.capacity
                
                # Check for high-risk nodes
                high_risk_nodes = [node_id for node_id, node in self.nodes.items() 
                                 if node.health_score < 0.6 or node.current_load / node.capacity > 0.9]
                
                # Generate cascade predictions for high-risk nodes
                for node_id in high_risk_nodes:
                    await self._generate_cascade_prediction(node_id)
                
                await asyncio.sleep(30)  # Monitor every 30 seconds
                
            except Exception as e:
                print(f"Monitoring error: {str(e)}")
                await asyncio.sleep(60)
    
    async def _generate_cascade_prediction(self, initial_failure_node: str):
        """Generate cascade failure prediction"""
        try:
            node = self.nodes[initial_failure_node]
            
            # Determine failure mode based on node condition
            if node.current_load / node.capacity > 0.9:
                failure_mode = FailureMode.OVERLOAD
            elif node.health_score < 0.6:
                failure_mode = FailureMode.EQUIPMENT_FAILURE
            else:
                failure_mode = FailureMode.STRUCTURAL_DAMAGE
            
            # Simulate cascade propagation
            cascade_result = self._simulate_cascade_propagation(initial_failure_node, failure_mode)
            
            # Calculate cascade radius
            affected_nodes = cascade_result["affected_nodes"]
            if affected_nodes:
                locations = [self.nodes[node_id].location for node_id in affected_nodes if node_id in self.nodes]
                if locations:
                    max_distance = max(
                        self._calculate_distance(self.nodes[initial_failure_node].location, loc)
                        for loc in locations
                    )
                else:
                    max_distance = 0
            else:
                max_distance = 0
            
            # Create prediction
            prediction = CascadePrediction(
                prediction_id=f"pred_{uuid.uuid4().hex[:12]}",
                timestamp=datetime.now(),
                initial_failure_node=initial_failure_node,
                failure_mode=failure_mode,
                cascade_probability=cascade_result["cascade_probability"],
                predicted_radius_km=max_distance,
                affected_nodes=affected_nodes,
                cascade_timeline=cascade_result["timeline"],
                total_impact_score=cascade_result["total_impact"],
                confidence=0.85
            )
            
            self.cascade_predictions.append(prediction)
            
            # Keep only recent predictions
            if len(self.cascade_predictions) > 100:
                self.cascade_predictions = self.cascade_predictions[-100:]
            
            # Generate pre-stabilization strategies if high risk
            if prediction.cascade_probability > 0.7:
                await self._generate_pre_stabilization_strategies(prediction)
            
        except Exception as e:
            print(f"Cascade prediction error for {initial_failure_node}: {str(e)}")
    
    def _simulate_cascade_propagation(self, initial_node: str, failure_mode: FailureMode) -> Dict[str, Any]:
        """Simulate cascade failure propagation"""
        affected_nodes = [initial_node]
        failed_nodes = set([initial_node])
        timeline = []
        current_time = 0
        total_impact = 0
        
        # Initial failure
        timeline.append({
            "time_minutes": current_time,
            "event": "initial_failure",
            "node": initial_node,
            "failure_mode": failure_mode.value,
            "impact_score": self.nodes[initial_node].criticality_score
        })
        total_impact += self.nodes[initial_node].criticality_score
        
        # Propagate failure through dependencies
        propagation_queue = deque([(initial_node, 0)])
        
        while propagation_queue:
            current_node, depth = propagation_queue.popleft()
            
            if depth > 5:  # Limit propagation depth
                continue
            
            current_time += 5  # 5 minutes per propagation step
            
            for dependent_id in self.nodes[current_node].dependents:
                if dependent_id not in failed_nodes:
                    edge_id = f"{current_node}_{dependent_id}"
                    if edge_id in self.edges:
                        edge = self.edges[edge_id]
                        
                        # Calculate failure probability
                        failure_prob = edge.failure_propagation_weight
                        
                        # Adjust based on node health and redundancy
                        dependent_node = self.nodes[dependent_id]
                        failure_prob *= (1 - dependent_node.health_score) * (1 - dependent_node.redundancy_level / 5)
                        
                        # Adjust based on failure mode
                        if failure_mode == FailureMode.OVERLOAD:
                            failure_prob *= 1.2
                        elif failure_mode == FailureMode.POWER_OUTAGE and dependent_node.node_type == NodeType.POWER_GRID:
                            failure_prob *= 1.5
                        
                        # Simulate failure
                        if np.random.random() < failure_prob:
                            failed_nodes.add(dependent_id)
                            affected_nodes.append(dependent_id)
                            
                            timeline.append({
                                "time_minutes": current_time,
                                "event": "cascade_failure",
                                "node": dependent_id,
                                "source_node": current_node,
                                "failure_probability": failure_prob,
                                "impact_score": dependent_node.criticality_score
                            })
                            
                            total_impact += dependent_node.criticality_score
                            propagation_queue.append((dependent_id, depth + 1))
        
        # Calculate overall cascade probability
        cascade_probability = min(1.0, len(failed_nodes) / len(self.nodes))
        
        return {
            "affected_nodes": affected_nodes,
            "cascade_probability": cascade_probability,
            "timeline": timeline,
            "total_impact": total_impact
        }
    
    def _calculate_distance(self, loc1: Dict[str, float], loc2: Dict[str, float]) -> float:
        """Calculate distance between two locations (simplified)"""
        lat_diff = loc1["lat"] - loc2["lat"]
        lon_diff = loc1["lon"] - loc2["lon"]
        return np.sqrt(lat_diff**2 + lon_diff**2) * 111  # Approximate km per degree
    
    async def _generate_pre_stabilization_strategies(self, prediction: CascadePrediction):
        """Generate pre-stabilization strategies"""
        strategies = []
        
        # Strategy 1: Stabilize critical nodes in cascade path
        critical_nodes = []
        for node_id in prediction.affected_nodes[:5]:  # Top 5 affected nodes
            if node_id in self.critical_node_analyses:
                analysis = self.critical_node_analyses[node_id]
                if analysis.stabilization_priority > 0.7:
                    critical_nodes.append(node_id)
        
        if critical_nodes:
            strategy = PreStabilizationStrategy(
                strategy_id=f"strategy_{uuid.uuid4().hex[:12]}",
                target_nodes=critical_nodes,
                stabilization_actions=[
                    {
                        "action_type": "load_reduction",
                        "target_nodes": critical_nodes,
                        "reduction_percentage": 0.3
                    },
                    {
                        "action_type": "backup_activation",
                        "target_nodes": critical_nodes[:2],
                        "backup_systems": 2
                    }
                ],
                expected_cascade_reduction=0.6,
                implementation_cost=50000,
                implementation_time_minutes=30,
                priority_score=0.8
            )
            strategies.append(strategy)
        
        # Strategy 2: Strengthen dependencies
        dependency_edges = []
        for node_id in prediction.affected_nodes[:3]:
            for dependent_id in self.nodes[node_id].dependents:
                if dependent_id in prediction.affected_nodes:
                    edge_id = f"{node_id}_{dependent_id}"
                    if edge_id in self.edges:
                        dependency_edges.append(edge_id)
        
        if dependency_edges:
            strategy = PreStabilizationStrategy(
                strategy_id=f"strategy_{uuid.uuid4().hex[:12]}",
                target_nodes=[edge.split("_")[1] for edge in dependency_edges],
                stabilization_actions=[
                    {
                        "action_type": "dependency_strengthening",
                        "target_edges": dependency_edges,
                        "strengthening_factor": 0.5
                    }
                ],
                expected_cascade_reduction=0.4,
                implementation_cost=30000,
                implementation_time_minutes=45,
                priority_score=0.6
            )
            strategies.append(strategy)
        
        # Store strategies
        for strategy in strategies:
            self.pre_stabilization_strategies[strategy.strategy_id] = strategy
    
    async def predict_cascade(self, initial_failure_node: str, failure_mode: str) -> Dict[str, Any]:
        """Predict cascade failure for specific node"""
        try:
            failure_mode_enum = FailureMode(failure_mode.lower())
            await self._generate_cascade_prediction(initial_failure_node)
            
            # Get latest prediction for this node
            for prediction in reversed(self.cascade_predictions):
                if prediction.initial_failure_node == initial_failure_node:
                    return prediction.to_dict()
            
            return {"error": "No prediction found for this node"}
            
        except ValueError:
            return {"error": f"Invalid failure mode: {failure_mode}"}
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    
    async def predict_cascade_failure(self, trigger_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict cascading failure probability combining real-time sensor data, 
        historical disaster probability, and infrastructure vulnerability
        """
        try:
            # Get real-time sensor data
            realtime_data = await self.get_realtime_sensor_data()
            
            # Get historical disaster probability for this region
            historical_prob = await self.get_historical_disaster_probability(trigger_event)
            
            # Get infrastructure vulnerability weights
            vulnerability_weights = self.get_infrastructure_vulnerability(trigger_event)
            
            # Calculate combined risk score (0-100)
            base_risk = trigger_event.get('severity', 0.5) * 50  # Convert severity to 0-100 scale
            
            # Add real-time sensor influence (30% weight)
            sensor_influence = realtime_data.get('anomaly_score', 0) * 0.3
            
            # Add historical probability influence (25% weight)
            historical_influence = historical_prob.get('probability', 0) * 25
            
            # Add infrastructure vulnerability influence (25% weight)
            vulnerability_influence = vulnerability_weights.get('vulnerability_score', 0) * 0.25
            
            # Combined risk score
            combined_risk_score = min(100, base_risk + sensor_influence + historical_influence + vulnerability_influence)
            
            # Calculate cascading failure probability
            cascade_probability = self.calculate_cascade_probability(
                combined_risk_score, 
                realtime_data.get('load_factor', 1.0),
                vulnerability_weights.get('dependency_density', 0.5)
            )
            
            # Calculate confidence based on data quality
            confidence = self.calculate_prediction_confidence([
                realtime_data.get('data_quality', 0.7),
                historical_prob.get('data_completeness', 0.8),
                len(vulnerability_weights.get('dependencies', [])) / 10  # Normalize dependency count
            ])
            
            # Generate prediction with explanation
            prediction = {
                'risk_score': round(combined_risk_score, 1),
                'prediction_confidence': round(confidence, 1),
                'cascading_failure_probability': round(cascade_probability, 3),
                'severity_level': self.get_severity_level(combined_risk_score),
                'affected_nodes': await self.predict_affected_nodes(trigger_event, cascade_probability),
                'time_to_cascade': self.estimate_time_to_cascade(cascade_probability),
                'mitigation_recommendations': self.generate_mitigation_recommendations(combined_risk_score, vulnerability_weights),
                'data_sources': {
                    'realtime_sensors': realtime_data.get('active_sensors', []),
                    'historical_data': historical_prob.get('source', 'unknown'),
                    'infrastructure_model': vulnerability_weights.get('model_version', '1.0')
                },
                'prediction_timestamp': datetime.datetime.now().isoformat(),
                'trigger_event': trigger_event
            }
            
            # Store prediction for learning
            await self.store_prediction_for_learning(prediction)
            
            return prediction
            
        except Exception as e:
            print(f"Error in cascade prediction: {e}")
            return {
                'risk_score': 50,
                'prediction_confidence': 30,
                'cascading_failure_probability': 25.0,
                'severity_level': 'medium',
                'error': str(e)
            }
        if probability > 0.8:
            return "critical"
        elif probability > 0.6:
            return "high"
        elif probability > 0.4:
            return "medium"
        else:
            return "low"
    
    async def get_realtime_sensor_data(self) -> Dict[str, Any]:
        """Get real-time sensor data from various sources"""
        try:
            # Simulate real-time sensor data
            # In production, this would pull from actual sensor APIs
            
            sensor_data = {
                'active_sensors': ['weather_stations', 'seismic_sensors', 'river_level_sensors', 'infrastructure_monitors'],
                'anomaly_score': round(random.uniform(0, 0.3), 2),  # Current anomaly level
                'load_factor': round(random.uniform(0.8, 1.2), 2),  # Current system load
                'data_quality': round(random.uniform(0.6, 0.9), 2),  # Sensor data quality
                'last_updated': datetime.datetime.now().isoformat()
            }
            
            return sensor_data
            
        except Exception as e:
            print(f"Error getting real-time sensor data: {e}")
            return {'anomaly_score': 0, 'load_factor': 1.0, 'data_quality': 0.7}
    
    async def get_historical_disaster_probability(self, trigger_event: Dict[str, Any]) -> Dict[str, Any]:
        """Get historical disaster probability for the event region"""
        try:
            # Simulate historical disaster probability based on location and type
            disaster_type = trigger_event.get('disaster_type', 'earthquake')
            location = trigger_event.get('location', 'mumbai')
            
            # Base probabilities for different regions in India
            historical_probabilities = {
                'mumbai': {'earthquake': 0.15, 'flood': 0.25, 'cyclone': 0.20},
                'delhi': {'earthquake': 0.12, 'flood': 0.18, 'cyclone': 0.15},
                'chennai': {'earthquake': 0.08, 'flood': 0.35, 'cyclone': 0.30},
                'kolkata': {'earthquake': 0.10, 'flood': 0.30, 'cyclone': 0.25},
                'bangalore': {'earthquake': 0.05, 'flood': 0.20, 'cyclone': 0.18}
            }
            
            location_probs = historical_probabilities.get(location, {'earthquake': 0.1})
            base_probability = location_probs.get(disaster_type, 0.1)
            
            # Adjust based on season (monsoon season increases flood probability)
            current_month = datetime.datetime.now().month
            if 6 <= current_month <= 9 and disaster_type == 'flood':  # Monsoon months
                base_probability *= 1.5
            
            return {
                'probability': round(base_probability, 3),
                'source': 'historical_analysis',
                'confidence': round(random.uniform(0.7, 0.9), 2),
                'data_completeness': round(random.uniform(0.6, 0.9), 2),
                'region': location,
                'disaster_type': disaster_type
            }
            
        except Exception as e:
            print(f"Error getting historical probability: {e}")
            return {'probability': 0.1, 'source': 'fallback'}
    
    def get_infrastructure_vulnerability(self, trigger_event: Dict[str, Any]) -> Dict[str, Any]:
        """Get infrastructure vulnerability weights for affected area"""
        try:
            location = trigger_event.get('location', 'mumbai')
            
            # Infrastructure vulnerability scores for different regions
            vulnerability_scores = {
                'mumbai': {
                    'vulnerability_score': 0.65,  # High density, aging infrastructure
                    'dependency_density': 0.8,
                    'critical_nodes': ['power_grid_mumbai', 'telecom_mumbai', 'transport_mumbai'],
                    'dependencies': 15,
                    'model_version': '2.1'
                },
                'delhi': {
                    'vulnerability_score': 0.55,  # Better infrastructure, but complex
                    'dependency_density': 0.7,
                    'critical_nodes': ['power_grid_delhi', 'telecom_delhi', 'transport_delhi'],
                    'dependencies': 18,
                    'model_version': '2.1'
                },
                'chennai': {
                    'vulnerability_score': 0.75,  # Coastal flooding vulnerability
                    'dependency_density': 0.6,
                    'critical_nodes': ['power_grid_chennai', 'telecom_chennai'],
                    'dependencies': 12,
                    'model_version': '2.1'
                }
            }
            
            return vulnerability_scores.get(location, {
                'vulnerability_score': 0.5,
                'dependency_density': 0.5,
                'critical_nodes': [],
                'dependencies': 10,
                'model_version': '1.0'
            })
            
        except Exception as e:
            print(f"Error getting infrastructure vulnerability: {e}")
            return {'vulnerability_score': 0.5, 'dependency_density': 0.5}
    
    def calculate_cascade_probability(self, risk_score: float, load_factor: float, dependency_density: float) -> float:
        """Calculate cascading failure probability"""
        try:
            # Base cascade probability from risk score
            base_probability = risk_score / 100
            
            # Adjust for system load (higher load = higher cascade risk)
            load_adjustment = load_factor * 0.2
            
            # Adjust for dependency density (more dependencies = higher cascade risk)
            dependency_adjustment = dependency_density * 0.15
            
            # Combined cascade probability
            cascade_probability = min(0.95, base_probability + load_adjustment + dependency_adjustment)
            
            return round(cascade_probability, 3)
            
        except Exception as e:
            print(f"Error calculating cascade probability: {e}")
            return 0.25
    
    def calculate_prediction_confidence(self, quality_factors: List[float]) -> float:
        """Calculate prediction confidence based on data quality factors"""
        try:
            # Weight the quality factors
            weights = [0.4, 0.3, 0.3]  # sensor, historical, dependency data
            
            # Calculate weighted average
            weighted_sum = sum(q * w for q, w in zip(quality_factors, weights))
            total_weight = sum(weights)
            
            if total_weight > 0:
                confidence = min(0.95, weighted_sum / total_weight)
            else:
                confidence = 0.5
            
            return round(confidence * 100, 1)
            
        except Exception as e:
            print(f"Error calculating prediction confidence: {e}")
            return 70.0
    
    async def predict_affected_nodes(self, trigger_event: Dict[str, Any], cascade_probability: float) -> List[str]:
        """Predict which infrastructure nodes will be affected by cascade"""
        try:
            location = trigger_event.get('location', 'mumbai')
            
            # Node vulnerability based on location
            location_nodes = {
                'mumbai': ['power_grid_mumbai', 'telecom_mumbai', 'transport_mumbai', 'hospital_mumbai', 'water_mumbai'],
                'delhi': ['power_grid_delhi', 'telecom_delhi', 'transport_delhi', 'hospital_delhi', 'water_delhi'],
                'chennai': ['power_grid_chennai', 'telecom_chennai'],
                'bangalore': ['power_grid_bangalore', 'telecom_bangalore']
            }
            
            affected_nodes = location_nodes.get(location, [])
            
            # Add nodes based on cascade probability
            if cascade_probability > 0.7:
                # High probability - affect more nodes
                affected_nodes.extend(affected_nodes[:2])  # Add 2 more critical nodes
            elif cascade_probability > 0.4:
                # Medium probability - affect 1 more node
                if len(affected_nodes) > 0:
                    affected_nodes.append(affected_nodes[0])
            
            return list(set(affected_nodes))  # Remove duplicates
            
        except Exception as e:
            print(f"Error predicting affected nodes: {e}")
            return trigger_event.get('affected_nodes', [])
    
    def estimate_time_to_cascade(self, cascade_probability: float) -> str:
        """Estimate time until cascade failure occurs"""
        try:
            if cascade_probability > 0.8:
                return "5-15 minutes"
            elif cascade_probability > 0.6:
                return "30-60 minutes"
            elif cascade_probability > 0.4:
                return "1-3 hours"
            elif cascade_probability > 0.2:
                return "3-6 hours"
            else:
                return "6-12 hours"
                
        except Exception as e:
            print(f"Error estimating time to cascade: {e}")
            return "Unknown"
    
    def generate_mitigation_recommendations(self, risk_score: float, vulnerability_weights: Dict[str, Any]) -> List[str]:
        """Generate mitigation recommendations based on risk and vulnerability"""
        try:
            recommendations = []
            
            if risk_score > 70:
                recommendations.extend([
                    "Activate emergency backup power systems",
                    "Deploy additional response teams",
                    "Initiate controlled load shedding",
                    "Alert neighboring regions for preparedness"
                ])
            
            if vulnerability_weights.get('vulnerability_score', 0) > 0.6:
                recommendations.extend([
                    "Inspect critical infrastructure joints",
                    "Pre-position repair equipment",
                    "Activate redundant communication channels"
                ])
            
            if risk_score > 50:
                recommendations.extend([
                    "Monitor system load in real-time",
                    "Prepare isolation procedures for critical nodes",
                    "Update emergency response protocols"
                ])
            
            # Remove duplicates
            return list(set(recommendations))
            
        except Exception as e:
            print(f"Error generating mitigation recommendations: {e}")
            return ["Monitor system status"]
    
    async def store_prediction_for_learning(self, prediction: Dict[str, Any]):
        """Store prediction for continuous learning improvement"""
        try:
            # Create learning data directory
            learning_dir = Path("data/learning_predictions")
            learning_dir.mkdir(exist_ok=True, parents=True)
            
            # Store prediction with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            prediction_file = learning_dir / f"prediction_{timestamp}.json"
            
            with open(prediction_file, 'w') as f:
                json.dump(prediction, f, indent=2)
            
            print(f"Stored prediction for learning: {prediction_file}")
            
        except Exception as e:
            print(f"Error storing prediction for learning: {e}")

    def _calculate_system_risk_level(self, cascade_probabilities: Dict[str, Any]) -> str:
        """Calculate overall system risk level"""
        if not cascade_probabilities:
            return "low"
        
        avg_probability = np.mean([prob["cascade_probability"] for prob in cascade_probabilities.values()])
        return self._get_risk_level(avg_probability)
    
    def get_critical_nodes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get critical nodes for pre-stabilization"""
        sorted_nodes = sorted(
            self.critical_node_analyses.items(),
            key=lambda x: x[1].stabilization_priority,
            reverse=True
        )
        
        return [analysis.to_dict() for node_id, analysis in sorted_nodes[:limit]]
    
    def get_pre_stabilization_strategies(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recommended pre-stabilization strategies"""
        sorted_strategies = sorted(
            self.pre_stabilization_strategies.values(),
            key=lambda x: x.priority_score,
            reverse=True
        )
        
        return [strategy.to_dict() for strategy in sorted_strategies[:limit]]
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get cascade forecast engine metrics"""
        return {
            "total_nodes": len(self.nodes),
            "total_dependencies": len(self.edges),
            "active_predictions": len(self.cascade_predictions),
            "critical_nodes_count": len([n for n in self.critical_node_analyses.values() if n.stabilization_priority > 0.7]),
            "available_strategies": len(self.pre_stabilization_strategies),
            "system_health": {
                "average_health_score": np.mean([node.health_score for node in self.nodes.values()]),
                "average_load_percentage": np.mean([node.current_load / node.capacity for node in self.nodes.values()]),
                "high_risk_nodes": len([n for n in self.nodes.values() if n.health_score < 0.6 or n.current_load / n.capacity > 0.9])
            },
            "timestamp": datetime.now().isoformat()
        }

# Global cascade forecast engine
cascade_forecast_engine = DigitalTwinCascadeForecastEngine()
