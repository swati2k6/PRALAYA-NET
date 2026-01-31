import { useState, useEffect } from "react";
import MapView from "../components/MapView";
import ControlPanel from "../components/ControlPanel";
import StatusPanel from "../components/StatusPanel";
import IntelligenceFeed from "../components/IntelligenceFeed";
import "../index.css";

const Dashboard = () => {
  const [systemStatus, setSystemStatus] = useState(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/trigger/status");
        const data = await response.json();
        setSystemStatus(data);
      } catch (error) {
        console.error("Error fetching system status:", error);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="command-center">
      <header className="command-header">
        <div className="header-left">
          <h1 className="system-title">PRALAYA-NET</h1>
          <span className="system-subtitle">Unified Disaster Command System</span>
        </div>
        <div className="header-right">
          <div className="mode-indicator">
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
