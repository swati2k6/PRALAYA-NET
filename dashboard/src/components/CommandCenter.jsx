import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { getBackendStatus } from '../config/api';

// Fix leaflet default icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const CommandCenter = () => {
  const [systemData, setSystemData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [systemMode, setSystemMode] = useState('autonomous');
  const [demoActive, setDemoActive] = useState(false);
  const [userLocation, setUserLocation] = useState([20.5937, 78.9629]); // Default to India coordinates

  // Fetch system data
  const fetchSystemData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/autonomous/command-center/data');
      if (response.ok) {
        const data = await response.json();
        setSystemData(data);
        setLoading(false);
      } else {
        throw new Error('Backend responded with error');
      }
    } catch (error) {
      console.error('Error fetching system data:', error);
      // Use mock data when backend is offline
      setSystemData(generateMockSystemData());
      setLoading(false);
    }
  };

  // Generate mock system data for simulation mode
  const generateMockSystemData = () => {
    const mockData = {
      national_stability_index: {
        value: 0.7 + Math.random() * 0.2, // 0.7 to 0.9
        status: Math.random() > 0.2 ? 'stable' : 'warning',
      },
      infrastructure: {
        nodes: {
          'power_grid_mumbai': { type: 'Power Grid', risk: Math.random(), load: Math.floor(Math.random() * 100), capacity: 100 },
          'power_grid_delhi': { type: 'Power Grid', risk: Math.random(), load: Math.floor(Math.random() * 100), capacity: 100 },
          'telecom_mumbai': { type: 'Telecom', risk: Math.random(), load: Math.floor(Math.random() * 100), capacity: 100 },
          'telecom_delhi': { type: 'Telecom', risk: Math.random(), load: Math.floor(Math.random() * 100), capacity: 100 },
          'transport_mumbai': { type: 'Transport', risk: Math.random(), load: Math.floor(Math.random() * 100), capacity: 100 },
          'transport_delhi': { type: 'Transport', risk: Math.random(), load: Math.floor(Math.random() * 100), capacity: 100 },
        }
      },
      autonomous_actions: {
        total_active: Math.floor(Math.random() * 10),
        executing: Math.floor(Math.random() * 5),
        completed_today: Math.floor(Math.random() * 20),
        active_intents: [
          { target_infrastructure_node: 'Power Grid Mumbai', status: Math.random() > 0.5 ? 'executing' : 'completed', risk_level: Math.random() },
          { target_infrastructure_node: 'Telecom Delhi', status: Math.random() > 0.5 ? 'executing' : 'pending', risk_level: Math.random() },
          { target_infrastructure_node: 'Transport Mumbai', status: 'completed', risk_level: Math.random() * 0.3 },
        ]
      },
      agent_coordination: {
        available: Math.floor(Math.random() * 20) + 5,
        total_agents: Math.floor(Math.random() * 10) + 25,
        agents: [
          { agent_id: 'DRONE-001', status: Math.random() > 0.3 ? 'executing' : 'idle', agent_type: 'Surveillance', performance_score: 0.8 + Math.random() * 0.2 },
          { agent_id: 'AGENT-002', status: Math.random() > 0.5 ? 'idle' : 'negotiating', agent_type: 'Coordination', performance_score: 0.7 + Math.random() * 0.3 },
          { agent_id: 'AGENT-003', status: 'completed', agent_type: 'Stabilization', performance_score: 0.9 + Math.random() * 0.1 },
        ]
      },
      execution_proof: {
        total_executions: Math.floor(Math.random() * 100) + 50,
        recent_ledger: [
          { intent_id: 'INTENT-' + Math.floor(Math.random() * 1000), validation_result: true, action_executed: 'Stabilize Power Grid', timestamp: Date.now() - 10000 },
          { intent_id: 'INTENT-' + Math.floor(Math.random() * 1000), validation_result: Math.random() > 0.2, action_executed: 'Route Traffic', timestamp: Date.now() - 30000 },
          { intent_id: 'INTENT-' + Math.floor(Math.random() * 1000), validation_result: true, action_executed: 'Allocate Resources', timestamp: Date.now() - 60000 },
        ]
      }
    };
    return mockData;
  };

  // Start autonomous demo
  const startAutonomousDemo = async () => {
    try {
      setDemoActive(true);
      const response = await fetch('http://127.0.0.1:8000/api/autonomous/start-autonomous-demo', {
        method: 'POST'
      });
      const result = await response.json();
      console.log('Demo started:', result);
    } catch (error) {
      console.error('Error starting demo:', error);
      setDemoActive(false);
    }
  };

  // Simulate disaster cascade
  const simulateDisaster = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/autonomous/simulate-disaster', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          disaster_type: 'earthquake',
          affected_nodes: ['power_grid_mumbai', 'telecom_mumbai', 'transport_mumbai'],
          severity: 0.8
        })
      });
      const result = await response.json();
      console.log('Disaster simulated:', result);
    } catch (error) {
      console.error('Error simulating disaster:', error);
    }
  };

  useEffect(() => {
    // Try to get user's geolocation on load
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          // Update map center to user's location
          setUserLocation([position.coords.latitude, position.coords.longitude]);
        },
        (error) => {
          console.log('Geolocation error or denied, using default coordinates');
          // Use default coordinates if geolocation is denied
          setUserLocation([20.5937, 78.9629]); // India coordinates
        },
        { timeout: 5000, enableHighAccuracy: true }
      );
    } else {
      // Geolocation not supported, use default coordinates
      setUserLocation([20.5937, 78.9629]); // India coordinates
    }
    
    fetchSystemData();
    const interval = setInterval(fetchSystemData, 3000); // Update every 3 seconds
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-xl">Loading Command Center...</div>
      </div>
    );
  }

  const getStabilityColor = (index) => {
    if (index < 0.4) return 'text-red-500';
    if (index < 0.7) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getStabilityBgColor = (index) => {
    if (index < 0.4) return 'bg-red-500';
    if (index < 0.7) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  // Infrastructure node locations
  const infrastructureLocations = {
    power_grid_mumbai: [19.0760, 72.8777],
    power_grid_delhi: [28.7041, 77.1025],
    telecom_mumbai: [19.0760, 72.8777],
    telecom_delhi: [28.7041, 77.1025],
    transport_mumbai: [19.0760, 72.8777],
    transport_delhi: [28.7041, 77.1025],
    water_mumbai: [19.0760, 72.8777],
    water_delhi: [28.7041, 77.1025],
    hospital_mumbai: [19.0760, 72.8777],
    hospital_delhi: [28.7041, 77.1025],
    bridge_sealink: [19.0760, 72.8777],
    bridge_bandra: [19.0760, 72.8777]
  };

  return (
    <div className="command-center">
      {/* Header */}
      <header className="command-header">
        <div className="header-left">
          <h1 className="system-title">🚀 PRALAYA-NET Command Center</h1>
          <span className="system-subtitle">Autonomous Self-Healing National Infrastructure Network</span>
        </div>
      </header>

      {/* Main Grid Layout */}
      <div className="command-grid">
        {/* Left Panel - Command Center */}
        <div className="command-panel">
          <h2 className="text-2xl font-bold mb-4">Command Center</h2>

          <div className="control-buttons">
            <button
              onClick={() => setSystemMode('manual')}
              className={`control-btn ${systemMode === 'manual' ? 'active' : ''}`}
            >
              🎮 Manual Mode
            </button>
            <button
              onClick={() => setSystemMode('assisted')}
              className={`control-btn ${systemMode === 'assisted' ? 'active' : ''}`}
            >
              🤖 Assisted Mode
            </button>
            <button
              onClick={() => setSystemMode('autonomous')}
              className={`control-btn ${systemMode === 'autonomous' ? 'active' : ''}`}
            >
              🚀 Autonomous Mode
            </button>
          </div>

          <div className="control-buttons">
            <button
              onClick={startAutonomousDemo}
              disabled={demoActive}
              className={`control-btn ${demoActive ? 'active' : ''}`}
            >
              {demoActive ? '⏸️ Demo Running...' : '▶️ Start Full Demo'}
            </button>
            <button
              onClick={simulateDisaster}
              className="control-btn danger"
            >
              🚨 Simulate Disaster
            </button>
          </div>

          {/* System Status */}
          <div className="panel-section">
            <div className="section-header">
              <span className="section-title">System Status</span>
            </div>
            <div className="status-item">
              <span className="status-label">Stability Index</span>
              <span className={`status-value ${systemData?.national_stability_index?.status === 'healthy' ? 'ok' : systemData?.national_stability_index?.status === 'warning' ? 'warning' : 'critical'}`}>
                {systemData?.national_stability_index?.status || 'Unknown'}
              </span>
            </div>
          </div>

          {/* Autonomous Actions */}
          <div className="panel-section">
            <div className="section-header">
              <span className="section-title">Autonomous Actions</span>
            </div>

            <div className="action-list">
              <div className="action-item">
                <div className="action-header">
                  <span className="action-title">Active Intents</span>
                  <span className="action-status">{systemData?.autonomous_actions?.total_active || 0}</span>
                </div>
                <div className="action-progress">
                  <div
                    className="action-progress-fill"
                    style={{ width: `${Math.min(100, (systemData?.autonomous_actions?.total_active || 0) * 20)}%` }}
                  ></div>
                </div>
              </div>

              <div className="action-item">
                <div className="action-header">
                  <span className="action-title">Executing</span>
                  <span className="action-status">{systemData?.autonomous_actions?.executing || 0}</span>
                </div>
                <div className="action-progress">
                  <div
                    className="action-progress-fill"
                    style={{ width: `${Math.min(100, (systemData?.autonomous_actions?.executing || 0) * 30)}%` }}
                  ></div>
                </div>
              </div>

              <div className="action-item">
                <div className="action-header">
                  <span className="action-title">Completed Today</span>
                  <span className="action-status">{systemData?.autonomous_actions?.completed_today || 0}</span>
                </div>
                <div className="action-progress">
                  <div
                    className="action-progress-fill"
                    style={{ width: `${Math.min(100, (systemData?.autonomous_actions?.completed_today || 0) * 5)}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Active Intents List */}
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-3">Active Intents</h3>
              <div className="action-list">
                {systemData?.autonomous_actions?.active_intents?.slice(0, 5).map((intent, index) => (
                  <div key={index} className="action-item">
                    <div className="action-header">
                      <span className="action-title">{intent.target_infrastructure_node}</span>
                      <span className={`action-status ${intent.status === 'executing' ? 'warning' : intent.status === 'completed' ? 'success' : 'info'}`}>
                        {intent.status}
                      </span>
                    </div>
                    <div className="text-gray-400 text-sm">
                      Risk: {(intent.risk_level * 100).toFixed(1)}%
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Center Panel - Risk Map */}
        <div className="map-container">
          <h2 className="text-2xl font-bold mb-4">India Infrastructure Risk Map</h2>
          <div className="leaflet-container">
            <MapContainer
              center={userLocation}
              zoom={5}
              style={{ height: '500px', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              />

              {/* Infrastructure nodes */}
              {systemData?.infrastructure?.nodes && Object.entries(systemData.infrastructure.nodes).map(([nodeId, nodeData]) => {
                const location = infrastructureLocations[nodeId];
                if (!location) return null;

                const risk = nodeData.risk;
                const color = risk > 0.6 ? '#dc2626' : risk > 0.3 ? '#f59e0b' : '#10b981';

                return (
                  <CircleMarker
                    key={nodeId}
                    center={location}
                    radius={10}
                    fillColor={color}
                    color="#fff"
                    weight={2}
                    opacity={1}
                    fillOpacity={0.8}
                  >
                    <Popup>
                      <div className="text-black">
                        <strong>{nodeId}</strong><br/>
                        Type: {nodeData.type}<br/>
                        Risk: {(risk * 100).toFixed(1)}%<br/>
                        Load: {nodeData.load}/{nodeData.capacity}
                      </div>
                    </Popup>
                  </CircleMarker>
                );
              })}
            </MapContainer>
          </div>
        </div>

        {/* Right Panel - Stability & Timeline */}
        <div className="right-panel">
          {/* Stability Index */}
          <div className="stability-panel">
            <h2 className="text-xl font-bold mb-4">National Stability Index</h2>
            <div className="stability-gauge">
              <div className={`stability-score ${getStabilityColor(systemData?.national_stability_index?.value || 0)}`}>
                {Math.round((systemData?.national_stability_index?.value || 0) * 100)}%
              </div>
              <div className="stability-label">
                {systemData?.national_stability_index?.status?.toUpperCase() || 'UNKNOWN'}
              </div>
              <div className="stability-bar">
                <div
                  className="stability-fill"
                  style={{
                    width: `${systemData?.national_stability_index?.value ? systemData.national_stability_index.value * 100 : 0}%`,
                    backgroundColor: getStabilityColor(systemData?.national_stability_index?.value || 0).replace('text-', '#')
                  }}
                ></div>
              </div>
            </div>
            <div className="text-center mt-4 text-gray-400 text-sm">
              Real-time infrastructure stability indicator
            </div>
          </div>

          {/* Agent Coordination */}
          <div className="timeline-panel">
            <h2 className="text-xl font-bold mb-4">Agent Coordination</h2>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-gray-700 rounded p-3">
                <div className="text-2xl font-bold text-green-400">
                  {systemData?.agent_coordination?.available || 0}
                </div>
                <div className="text-gray-400 text-sm">Available Agents</div>
              </div>
              <div className="bg-gray-700 rounded p-3">
                <div className="text-2xl font-bold text-yellow-400">
                  {systemData?.agent_coordination?.total_agents || 0}
                </div>
                <div className="text-gray-400 text-sm">Total Agents</div>
              </div>
            </div>

            <h3 className="text-lg font-semibold mb-3">Agent Status</h3>
            <div className="action-list">
              {systemData?.agent_coordination?.agents?.slice(0, 4).map((agent, index) => (
                <div key={index} className="action-item">
                  <div className="action-header">
                    <span className="action-title">{agent.agent_id}</span>
                    <span className={`action-status ${agent.status === 'idle' ? 'success' : agent.status === 'executing' ? 'warning' : 'info'}`}>
                      {agent.status}
                    </span>
                  </div>
                  <div className="text-gray-400 text-sm">
                    {agent.agent_type} • Performance: {(agent.performance_score * 100).toFixed(1)}%
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Crisis Timeline Feed */}
          <div className="timeline-panel">
            <h2 className="text-xl font-bold mb-4">Crisis Timeline Feed</h2>
            <div className="timeline-list">
              <div className="timeline-event">
                <div className="event-indicator critical"></div>
                <div className="event-content">
                  <div className="event-title">Disaster Detected</div>
                  <div className="event-description">High risk detected in Mumbai power grid</div>
                  <div className="event-time">{new Date().toLocaleString()}</div>
                </div>
              </div>

              <div className="timeline-event">
                <div className="event-indicator warning"></div>
                <div className="event-content">
                  <div className="event-title">Intent Generated</div>
                  <div className="event-description">Autonomous stabilization intent created</div>
                  <div className="event-time">{new Date().toLocaleString()}</div>
                </div>
              </div>

              <div className="timeline-event">
                <div className="event-indicator info"></div>
                <div className="event-content">
                  <div className="event-title">Agents Negotiating</div>
                  <div className="event-description">Multi-agent negotiation in progress</div>
                  <div className="event-time">{new Date().toLocaleString()}</div>
                </div>
              </div>

              <div className="timeline-event">
                <div className="event-indicator success"></div>
                <div className="event-content">
                  <div className="event-title">Infrastructure Stabilized</div>
                  <div className="event-description">Risk reduced by 45%, stability improved</div>
                  <div className="event-time">{new Date().toLocaleString()}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Execution Proof */}
          <div className="timeline-panel">
            <h2 className="text-xl font-bold mb-4">Execution Proof</h2>
            <div className="bg-gray-700 rounded p-3 mb-4">
              <div className="text-2xl font-bold text-blue-400">
                {systemData?.execution_proof?.total_executions || 0}
              </div>
              <div className="text-gray-400 text-sm">Executions Today</div>
            </div>

            <h3 className="text-lg font-semibold mb-3">Recent Ledger Entries</h3>
            <div className="action-list">
              {systemData?.execution_proof?.recent_ledger?.slice(0, 3).map((entry, index) => (
                <div key={index} className="action-item">
                  <div className="action-header">
                    <span className="action-title">{entry.intent_id}</span>
                    <span className={`action-status ${entry.validation_result ? 'success' : 'critical'}`}>
                      {entry.validation_result ? 'Success' : 'Failed'}
                    </span>
                  </div>
                  <div className="text-gray-400 text-sm">
                    {entry.action_executed}
                  </div>
                  <div className="text-gray-500 text-xs">
                    {new Date(entry.timestamp).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CommandCenter;
