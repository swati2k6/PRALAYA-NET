import { useState, useEffect } from "react";
import MapView from "../components/MapView";
import ControlPanel from "../components/ControlPanel";
import StatusPanel from "../components/StatusPanel";
import IntelligenceFeed from "../components/IntelligenceFeed";
import { checkBackendHealth } from "../services/api";
import "../index.css";

const Dashboard = () => {
  const [systemStatus, setSystemStatus] = useState(null);
  const [backendOnline, setBackendOnline] = useState(false);
  const [connectionError, setConnectionError] = useState(null);

  // Check backend health on mount
  useEffect(() => {
    const initBackend = async () => {
      try {
        const isHealthy = await checkBackendHealth();
        setBackendOnline(isHealthy);
        
        if (!isHealthy) {
          setConnectionError("Backend offline - waiting for connection...");
          console.error("[Dashboard] Backend is not responding");
        } else {
          setConnectionError(null);
          console.log("[Dashboard] Backend is online");
        }
      } catch (error) {
        console.error("[Dashboard] Failed to initialize backend:", error);
        setBackendOnline(false);
        setConnectionError(error.message);
      }
    };

    initBackend();
    
    // Check backend health every 30 seconds
    const healthCheckInterval = setInterval(initBackend, 30000);
    return () => clearInterval(healthCheckInterval);
  }, []);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/trigger/status");
        const data = await response.json();
        setSystemStatus(data);
        setBackendOnline(true);
        setConnectionError(null);
      } catch (error) {
        console.error("[Dashboard] Error fetching system status:", error.message);
        setBackendOnline(false);
        setConnectionError("Failed to fetch system status - backend unreachable");
      }
    };

    if (backendOnline) {
      fetchStatus();
      const interval = setInterval(fetchStatus, 5000);
      return () => clearInterval(interval);
    }
  }, [backendOnline]);

  return (
    <div className="command-center">
      {/* Backend Connection Error Banner */}
      {!backendOnline && (
        <div style={{
          backgroundColor: "#ff4444",
          color: "white",
          padding: "12px 20px",
          textAlign: "center",
          fontWeight: "bold",
          borderBottom: "2px solid #cc0000",
          zIndex: 1000
        }}>
          🔴 BACKEND OFFLINE: {connectionError || "Unable to connect to backend server at http://127.0.0.1:8000"}
        </div>
      )}

      <header className="command-header">
        <div className="header-left">
          <h1 className="system-title">PRALAYA-NET</h1>
          <span className="system-subtitle">Unified Disaster Command System</span>
        </div>
        <div className="header-right">
          {/* Backend Status Indicator */}
          <div className="mode-indicator">
            <span style={{ marginRight: "15px", display: "flex", alignItems: "center", gap: "5px" }}>
              <span style={{ 
                width: "12px", 
                height: "12px", 
                borderRadius: "50%", 
                backgroundColor: backendOnline ? "#00ff00" : "#ff4444",
                display: "inline-block"
              }}></span>
              Backend: {backendOnline ? "ONLINE" : "OFFLINE"}
            </span>
            <span className="mode-label">SIMULATION MODE</span>
            <span className="mode-status">LIVE DATA READY</span>
          </div>
          <div className="timestamp">
            {new Date().toLocaleString('en-US', {
              hour12: false,
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit'
            })}
          </div>
        </div>
      </header>

      <div className="command-grid">
        {/* LEFT PANEL - Control & Status */}
        <aside className="panel-left">
          <ControlPanel />
          <StatusPanel systemStatus={systemStatus} />
        </aside>

        {/* CENTER PANEL - Geospatial Map */}
        <main className="panel-center">
          <MapView />
        </main>

        {/* RIGHT PANEL - Intelligence Feed */}
        <aside className="panel-right">
          <IntelligenceFeed systemStatus={systemStatus} />
        </aside>
      </div>

      <footer className="command-footer">
        <div className="footer-left">
          <span>System Status: OPERATIONAL</span>
          <span className="footer-separator">|</span>
          <span>Version 1.0.0</span>
        </div>
        <div className="footer-right">
          <span>NDMA / ISRO Compatible Architecture</span>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
