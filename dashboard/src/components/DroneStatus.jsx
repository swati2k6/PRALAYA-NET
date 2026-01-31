import { useEffect, useState } from "react";
import { getDroneStatus, getDroneTelemetry } from "../services/api";

const DroneStatus = () => {
  const [drones, setDrones] = useState([]);
  const [selectedDrone, setSelectedDrone] = useState(null);
  const [telemetry, setTelemetry] = useState(null);

  useEffect(() => {
    const fetchDrones = async () => {
      try {
        const status = await getDroneStatus();
        setDrones(status.drones || []);
        
        if (status.drones && status.drones.length > 0 && !selectedDrone) {
          setSelectedDrone(status.drones[0].id);
        }
      } catch (error) {
        console.error("Error fetching drone status:", error);
      }
    };

    fetchDrones();
    const interval = setInterval(fetchDrones, 2000); // Update every 2 seconds

    return () => clearInterval(interval);
  }, [selectedDrone]);

  useEffect(() => {
    if (!selectedDrone) return;

    const fetchTelemetry = async () => {
      try {
        const data = await getDroneTelemetry(selectedDrone);
        setTelemetry(data);
      } catch (error) {
        console.error("Error fetching telemetry:", error);
      }
    };

    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 2000);

    return () => clearInterval(interval);
  }, [selectedDrone]);

  const getStatusColor = (status) => {
    const colors = {
      active: "#22c55e",
      flying: "#3b82f6",
      landed: "#6b7280",
      error: "#dc2626",
    };
    return colors[status] || "#6b7280";
  };

  return (
    <div className="drone-status-container">
      <h2>🚁 Drone Fleet Status</h2>
      
      <div className="drone-list">
        {drones.length === 0 ? (
          <p>No drones deployed</p>
        ) : (
          drones.map((drone) => (
            <div
              key={drone.id}
              className={`drone-card ${selectedDrone === drone.id ? "selected" : ""}`}
              onClick={() => setSelectedDrone(drone.id)}
            >
              <div className="drone-header">
                <strong>{drone.id}</strong>
                <span
                  className="status-badge"
                  style={{ backgroundColor: getStatusColor(drone.status) }}
                >
                  {drone.status}
                </span>
              </div>
              <div className="drone-info">
                <div>Battery: {drone.battery?.toFixed(1) || 0}%</div>
                <div>SLAM: {drone.slam_enabled ? "✅ Enabled" : "❌ Disabled"}</div>
              </div>
            </div>
          ))
        )}
      </div>

      {telemetry && (
        <div className="telemetry-panel">
          <h3>📊 Telemetry - {selectedDrone}</h3>
          <div className="telemetry-grid">
            <div className="telemetry-item">
              <label>Location</label>
              <div>
                {telemetry.location?.lat?.toFixed(4)}, {telemetry.location?.lon?.toFixed(4)}
              </div>
            </div>
            <div className="telemetry-item">
              <label>Altitude</label>
              <div>{telemetry.altitude?.toFixed(1)} m</div>
            </div>
            <div className="telemetry-item">
              <label>Speed</label>
              <div>{telemetry.speed?.toFixed(1)} m/s</div>
            </div>
            <div className="telemetry-item">
              <label>Heading</label>
              <div>{telemetry.heading?.toFixed(1)}°</div>
            </div>
            <div className="telemetry-item">
              <label>Battery</label>
              <div>{telemetry.battery?.toFixed(1)}%</div>
            </div>
            <div className="telemetry-item">
              <label>Signal</label>
              <div>{telemetry.signal_strength?.toFixed(1)}%</div>
            </div>
            <div className="telemetry-item">
              <label>GPS Status</label>
              <div className={telemetry.gps_status === "active" ? "status-ok" : "status-warning"}>
                {telemetry.gps_status}
              </div>
            </div>
            <div className="telemetry-item">
              <label>V-SLAM Status</label>
              <div className={telemetry.slam_status === "active" ? "status-ok" : "status-info"}>
                {telemetry.slam_status}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DroneStatus;
