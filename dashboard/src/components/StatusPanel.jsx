import { useEffect, useState } from "react";
import { getSystemStatus } from "../services/api";

const StatusPanel = ({ systemStatus }) => {
  const [status, setStatus] = useState(systemStatus);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await getSystemStatus();
        setStatus(data);
      } catch (error) {
        console.error("Error fetching status:", error);
        // Don't show error to user, just log it
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!status) {
    return (
      <div className="panel-section">
        <div className="section-header">
          <span className="section-title">System Status</span>
        </div>
        <div className="empty-state">Initializing...</div>
      </div>
    );
  }

  const systemHealth = status.system_health || {};
  const activeDisasters = status.active_disasters || [];
  const pendingAlerts = status.pending_alerts || 0;

  return (
    <>
      {/* System Health */}
      <div className="panel-section">
        <div className="section-header">
          <span className="section-title">System Health</span>
          <span className="section-badge">ONLINE</span>
        </div>
        <div className="status-item">
          <span className="status-label">AI Models</span>
          <span className="status-value ok">{systemHealth.ai_models || "OPERATIONAL"}</span>
        </div>
        <div className="status-item">
          <span className="status-label">Orchestration</span>
          <span className="status-value ok">{systemHealth.orchestration || "OPERATIONAL"}</span>
        </div>
        <div className="status-item">
          <span className="status-label">Hardware</span>
          <span className="status-value ok">{systemHealth.hardware || "CONNECTED"}</span>
        </div>
      </div>

      {/* Space Weather */}
      <div className="panel-section">
        <div className="section-header">
          <span className="section-title">Space Weather</span>
        </div>
        {status.cascading_analysis?.initial_disaster && (
          <>
            <div className="status-item">
              <span className="status-label">GPS Status</span>
              <span className={`status-value ${status.cascading_analysis.initial_disaster.type === 'cyclone' || status.cascading_analysis.initial_disaster.type === 'earthquake' ? 'warning' : 'ok'}`}>
                {status.cascading_analysis.initial_disaster.type === 'cyclone' || status.cascading_analysis.initial_disaster.type === 'earthquake' ? 'DEGRADED' : 'OPERATIONAL'}
              </span>
            </div>
            <div className="status-item">
              <span className="status-label">Comms Status</span>
              <span className="status-value ok">OPERATIONAL</span>
            </div>
          </>
        )}
        {!status.cascading_analysis?.initial_disaster && (
          <>
            <div className="status-item">
              <span className="status-label">GPS Status</span>
              <span className="status-value ok">OPERATIONAL</span>
            </div>
            <div className="status-item">
              <span className="status-label">Comms Status</span>
              <span className="status-value ok">OPERATIONAL</span>
            </div>
          </>
        )}
      </div>

      {/* Active Situations */}
      <div className="panel-section">
        <div className="section-header">
          <span className="section-title">Active Situations</span>
          <span className="section-badge">{activeDisasters.length}</span>
        </div>
        {activeDisasters.length === 0 ? (
          <div className="empty-state">No active disasters</div>
        ) : (
          activeDisasters.map((disaster) => (
            <div key={disaster.id} className="status-item">
              <span className="status-label">{disaster.type.toUpperCase()}</span>
              <span className={`status-value ${disaster.severity >= 0.8 ? 'critical' : disaster.severity >= 0.6 ? 'warning' : 'info'}`}>
                {(disaster.severity * 100).toFixed(0)}%
              </span>
            </div>
          ))
        )}
      </div>

      {/* Alert Queue */}
      <div className="panel-section">
        <div className="section-header">
          <span className="section-title">Alert Queue</span>
          <span className="section-badge">{pendingAlerts}</span>
        </div>
        <div className="status-item">
          <span className="status-label">Pending</span>
          <span className={`status-value ${pendingAlerts > 0 ? 'warning' : 'ok'}`}>
            {pendingAlerts}
          </span>
        </div>
      </div>
    </>
  );
};

export default StatusPanel;
