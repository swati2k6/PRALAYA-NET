import { useEffect, useState } from "react";
import { getSystemStatus } from "../services/api";

const RiskGraph = () => {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [criticalNodes, setCriticalNodes] = useState([]);

  useEffect(() => {
    const fetchGraph = async () => {
      try {
        const status = await getSystemStatus();
        if (status.cascading_analysis?.graph) {
          setGraphData(status.cascading_analysis.graph);
          setCriticalNodes(status.cascading_analysis.critical_nodes || []);
        }
      } catch (error) {
        console.error("Error fetching risk graph:", error);
      }
    };

    fetchGraph();
    const interval = setInterval(fetchGraph, 5000); // Update every 5 seconds

    return () => clearInterval(interval);
  }, []);

  const getRiskColor = (risk) => {
    if (risk >= 0.8) return "#dc2626"; // red
    if (risk >= 0.6) return "#ea580c"; // orange
    if (risk >= 0.3) return "#eab308"; // yellow
    return "#22c55e"; // green
  };

  const getRiskLevel = (risk) => {
    if (risk >= 0.8) return "CRITICAL";
    if (risk >= 0.6) return "HIGH";
    if (risk >= 0.3) return "MEDIUM";
    return "LOW";
  };

  return (
    <div className="risk-graph-container">
      <h2>🕸️ Cascading Risk Analysis (GNN)</h2>
      
      {graphData.nodes.length === 0 ? (
        <div className="empty-state">
          <p>No active risks detected. System is monitoring...</p>
        </div>
      ) : (
        <>
          <div className="graph-nodes">
            {graphData.nodes.map((node) => (
              <div
                key={node.id}
                className="graph-node"
                style={{
                  borderColor: getRiskColor(node.risk),
                  backgroundColor: `${getRiskColor(node.risk)}20`,
                }}
              >
                <div className="node-header">
                  <strong>{node.name}</strong>
                  <span className={`risk-badge risk-${node.risk_level}`}>
                    {getRiskLevel(node.risk)}
                  </span>
                </div>
                <div className="node-details">
                  <div>Type: {node.type}</div>
                  <div>Risk Score: {(node.risk * 100).toFixed(1)}%</div>
                </div>
              </div>
            ))}
          </div>

          {criticalNodes.length > 0 && (
            <div className="critical-alert">
              <h3>⚠️ Critical Infrastructure at Risk</h3>
              <ul>
                {criticalNodes.map((node) => (
                  <li key={node.id}>
                    <strong>{node.name}</strong> - Risk: {(node.risk * 100).toFixed(1)}%
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="graph-legend">
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: "#22c55e" }}></span>
              Low Risk (&lt;30%)
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: "#eab308" }}></span>
              Medium Risk (30-60%)
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: "#ea580c" }}></span>
              High Risk (60-80%)
            </div>
            <div className="legend-item">
              <span className="legend-color" style={{ backgroundColor: "#dc2626" }}></span>
              Critical Risk (&gt;80%)
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default RiskGraph;
