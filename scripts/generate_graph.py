#!/usr/bin/env python3
"""
Graph Generator - Generate cascading risk graphs
"""

import json
import networkx as nx
from datetime import datetime

def generate_cascading_graph(output_path="data/simulated/cascading.json"):
    """
    Generate a cascading failure graph structure
    
    Args:
        output_path: Path to save the graph JSON
    """
    # Create graph
    G = nx.DiGraph()
    
    # Infrastructure nodes
    nodes = [
        {"id": "power_grid_1", "name": "Power Grid Station A", "type": "power", "lat": 28.6139, "lon": 77.2090},
        {"id": "hospital_1", "name": "City Hospital", "type": "healthcare", "lat": 28.7041, "lon": 77.1025},
        {"id": "water_supply_1", "name": "Water Treatment Plant", "type": "water", "lat": 28.5355, "lon": 77.3910},
        {"id": "telecom_1", "name": "Telecom Tower", "type": "telecom", "lat": 28.5562, "lon": 77.1000},
    ]
    
    # Add nodes
    for node in nodes:
        G.add_node(node["id"], **node)
    
    # Add edges (dependencies)
    edges = [
        ("power_grid_1", "hospital_1", {"weight": 0.9, "type": "power_dependency"}),
        ("power_grid_1", "water_supply_1", {"weight": 0.8, "type": "power_dependency"}),
        ("power_grid_1", "telecom_1", {"weight": 0.7, "type": "power_dependency"}),
        ("water_supply_1", "hospital_1", {"weight": 0.6, "type": "water_dependency"}),
        ("water_supply_1", "telecom_1", {"weight": 0.5, "type": "water_dependency"}),
        ("telecom_1", "hospital_1", {"weight": 0.4, "type": "communication_dependency"}),
    ]
    
    for source, target, data in edges:
        G.add_edge(source, target, **data)
    
    # Convert to JSON-serializable format
    graph_data = {
        "nodes": [
            {
                "id": node,
                **G.nodes[node]
            }
            for node in G.nodes()
        ],
        "edges": [
            {
                "source": source,
                "target": target,
                **G[source][target]
            }
            for source, target in G.edges()
        ],
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "node_count": len(G.nodes()),
            "edge_count": len(G.edges())
        }
    }
    
    # Save to file
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(graph_data, f, indent=2)
    
    print(f"✅ Graph generated: {output_path}")
    print(f"   Nodes: {len(graph_data['nodes'])}")
    print(f"   Edges: {len(graph_data['edges'])}")
    
    return graph_data

if __name__ == "__main__":
    generate_cascading_graph()



