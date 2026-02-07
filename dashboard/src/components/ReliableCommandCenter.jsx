import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { API_ENDPOINTS, WS_ENDPOINTS, CONFIG } from '../config/api';
import '../styles/CommandCenter.css';

// Fix leaflet default icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const ReliableCommandCenter = () => {
  const [systemData, setSystemData] = useState(null);
  const [stabilityData, setStabilityData] = useState(null);
  const [timelineEvents, setTimelineEvents] = useState([]);
  const [activeActions, setActiveActions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [systemMode, setSystemMode] = useState('autonomous');
  const [demoActive, setDemoActive] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [backendStatus, setBackendStatus] = useState('checking');
  
  // WebSocket connections
  const stabilityWs = useRef(null);
  const actionsWs = useRef(null);
  const timelineWs = useRef(null);
  const riskWs = useRef(null);

  // Helper functions
  const getStabilityColor = (index) => {
    if (!index) return 'text-gray-500';
    if (index.overall_score < 0.4) return 'text-red-500';
    if (index.overall_score < 0.7) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getRiskColor = (risk) => {
    if (risk > 0.8) return '#dc2626';
    if (risk > 0.6) return '#f59e0b';
    if (risk > 0.4) return '#3b82f6';
    return '#10b981';
  };

  // Initialize WebSocket connections and health checking
  useEffect(() => {
    // Start backend health checking every 5 seconds
    const healthCheckInterval = setInterval(async () => {
      try {
        const response = await fetch(API_ENDPOINTS.HEALTH);
        if (response.ok) {
          setBackendStatus('online');
          setConnectionStatus('connected');
        } else {
          setBackendStatus('offline');
          setConnectionStatus('error');
        }
      } catch (error) {
        setBackendStatus('offline');
        setConnectionStatus('error');
        console.error('Backend health check failed:', error);
      }
    }, CONFIG.HEALTH_CHECK_INTERVAL);

    // Initial data fetch
    fetchInitialData();
    
    // Connect to WebSocket streams
    connectWebSockets();
    
    return () => {
      // Cleanup interval and WebSocket connections
      clearInterval(healthCheckInterval);
      if (stabilityWs.current) stabilityWs.current.close();
      if (actionsWs.current) actionsWs.current.close();
      if (timelineWs.current) timelineWs.current.close();
      if (riskWs.current) riskWs.current.close();
    };
  }, []);

  const connectWebSockets = () => {
    console.log('🔄 Connecting to WebSocket streams...');
    
    // Stability stream
    stabilityWs.current = new WebSocket(WS_ENDPOINTS.STABILITY_STREAM);
    stabilityWs.current.onopen = () => {
      console.log('✅ Connected to stability stream');
      setConnectionStatus('connected');
    };
    stabilityWs.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'stability_update') {
        setStabilityData(data.data);
      }
    };
    stabilityWs.current.onerror = (error) => {
      console.error('❌ Stability stream error:', error);
      setConnectionStatus('error');
    };

    // Actions stream
    actionsWs.current = new WebSocket(WS_ENDPOINTS.ACTIONS_STREAM);
    actionsWs.current.onopen = () => {
      console.log('✅ Connected to actions stream');
    };
    actionsWs.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'action_update') {
        setActiveActions(prev => [...prev.slice(-9), data.data]);
      }
    };
    actionsWs.current.onerror = (error) => {
      console.error('❌ Actions stream error:', error);
    };

    // Timeline stream
    timelineWs.current = new WebSocket(WS_ENDPOINTS.TIMELINE_STREAM);
    timelineWs.current.onopen = () => {
      console.log('✅ Connected to timeline stream');
    };
    timelineWs.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'event') {
        setTimelineEvents(prev => [...prev.slice(-19), data.data]);
      }
    };
    timelineWs.current.onerror = (error) => {
      console.error('❌ Timeline stream error:', error);
    };

    // Risk stream
    riskWs.current = new WebSocket(WS_ENDPOINTS.RISK_STREAM);
    riskWs.current.onopen = () => {
      console.log('✅ Connected to risk stream');
    };
    riskWs.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'risk_update') {
        // Update system data with risk information
        setSystemData(prev => prev ? {
          ...prev,
          current_risk: data.data
        } : { current_risk: data.data });
      }
    };
    riskWs.current.onerror = (error) => {
      console.error('❌ Risk stream error:', error);
    };
  };

  const fetchInitialData = async () => {
    try {
      setBackendStatus('checking');
      console.log('🔄 Connecting to PRALAYA-NET backend...');
      
      // Fetch system data
      const systemResponse = await fetch(API_ENDPOINTS.SYSTEM_STATUS);
      const systemData = await systemResponse.json();
      setSystemData(systemData);

      // Fetch stability data
      const stabilityResponse = await fetch(API_ENDPOINTS.STABILITY_CURRENT);
      const stabilityData = await stabilityResponse.json();
      setStabilityData(stabilityData.stability_index);

      // Fetch risk data
      const riskResponse = await fetch(API_ENDPOINTS.RISK_PREDICT);
      const riskData = await riskResponse.json();
      
      setBackendStatus('online');
      console.log('✅ Connected to PRALAYA-NET backend');
      setLoading(false);
    } catch (error) {
      console.error('❌ Error connecting to backend:', error);
      setBackendStatus('offline');
      setLoading(false);
    }
  };

  const simulateDisaster = async () => {
    try {
      const response = await fetch(API_ENDPOINTS.RISK_PREDICT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          disaster_type: 'earthquake',
          severity: 0.8
        })
      });
      const result = await response.json();
      console.log('Disaster simulated:', result);
    } catch (error) {
      console.error('Error simulating disaster:', error);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-text">Loading PRALAYA-NET Command Center...</div>
        <div className="loading-status">
          <div className="loading-spinner"></div>
          <span>
            {backendStatus === 'checking' ? 'Checking backend connection...' : 
             backendStatus === 'online' ? 'Backend connected' : 
             'Backend offline - check if backend is running'}
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="command-center">
      {/* Header */}
      <header className="command-header">
        <div className="flex items-center justify-between mb-2">
          <h1 className="text-4xl font-bold">🚀 PRALAYA-NET Command Center</h1>
          <div className="status-indicators">
            <div className="flex items-center space-x-2">
              <div className={`status-dot ${connectionStatus}`}></div>
              <span className="status-text">
                {connectionStatus === 'connected' ? '✅ Connected' : 
                 connectionStatus === 'error' ? '❌ Connection Error' : 
                 '🔄 Reconnecting...'}
              </span>
            </div>
            <div className="flex items-center space-x-2">
              <div className={`status-dot ${backendStatus === 'online' ? 'connected' : backendStatus === 'offline' ? 'error' : 'reconnecting'}`}></div>
              <span className="status-text">
                Backend: {backendStatus === 'online' ? '🟢 Online' : 
                       backendStatus === 'offline' ? '🔴 Offline' : 
                       '🟡 Checking...'}
              </span>
            </div>
          </div>
        </div>
        <p className="text-gray-400">Reliable Autonomous Disaster-Response Command Platform</p>
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
              onClick={() => setSystemMode('autonomous')}
              className={`control-btn ${systemMode === 'autonomous' ? 'active' : ''}`}
            >
              🤖 Autonomous Mode
            </button>
          </div>

          <div className="control-buttons">
            <button
              onClick={simulateDisaster}
              className="control-btn danger"
              disabled={demoActive}
            >
              🚨 Simulate Disaster
            </button>
            <button
              onClick={() => setDemoActive(!demoActive)}
              className={`control-btn ${demoActive ? 'active' : ''}`}
            >
              {demoActive ? '⏸️ Demo Running...' : '▶️ Start Demo'}
            </button>
          </div>

          {/* Active Actions */}
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-3">Active Autonomous Actions</h3>
            <div className="action-list">
              {activeActions.length === 0 ? (
                <div className="text-gray-400 text-center py-8">
                  No active actions - {systemMode === 'autonomous' ? 'waiting for autonomous response' : 'switch to autonomous mode'}
                </div>
              ) : (
                activeActions.map((action, index) => (
                  <div key={index} className="action-item">
                    <div className="action-header">
                      <span className="action-title">{action.action_type}</span>
                      <span className="action-status">{action.status}</span>
                    </div>
                    <div className="action-description text-sm text-gray-400 mb-2">
                      {action.description}
                    </div>
                    <div className="action-progress">
                      <div 
                        className="action-progress-fill" 
                        style={{ width: `${action.progress || 0}%` }}
                      ></div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Center Panel - Risk Map */}
        <div className="map-container">
          <h2 className="text-2xl font-bold mb-4">India Infrastructure Risk Map</h2>
          <div className="leaflet-container">
            <MapContainer
              center={[20.5937, 78.9629]}
              zoom={5}
              style={{ height: '500px', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              />
              
              {/* Sample infrastructure nodes */}
              <CircleMarker
                center={[19.0760, 72.8777]} // Mumbai
                radius={50000}
                fillColor={getRiskColor(0.6)}
                color={getRiskColor(0.6)}
                weight={2}
                opacity={0.6}
              >
                <Popup>
                  <div className="text-sm">
                    <strong>Mumbai Infrastructure</strong><br/>
                    Risk: 60%<br/>
                    Status: Active Monitoring
                  </div>
                </Popup>
              </CircleMarker>
              
              <CircleMarker
                center={[28.7041, 77.1025]} // Delhi
                radius={40000}
                fillColor={getRiskColor(0.4)}
                color={getRiskColor(0.4)}
                weight={2}
                opacity={0.6}
              >
                <Popup>
                  <div className="text-sm">
                    <strong>Delhi Infrastructure</strong><br/>
                    Risk: 40%<br/>
                    Status: Normal
                  </div>
                </Popup>
              </CircleMarker>
            </MapContainer>
          </div>
        </div>

        {/* Right Panel - Stability & Timeline */}
        <div className="right-panel">
          {/* Stability Index */}
          <div className="stability-panel">
            <h2 className="text-xl font-bold mb-4">National Stability Index</h2>
            <div className="stability-gauge">
              <div className={`stability-score ${getStabilityColor(stabilityData)}`}>
                {stabilityData?.overall_score ? (stabilityData.overall_score * 100).toFixed(1) : '0.0'}%
              </div>
              <div className="stability-label">
                {stabilityData?.level?.toUpperCase() || 'UNKNOWN'}
              </div>
              <div className="stability-bar">
                <div 
                  className="stability-fill" 
                  style={{ 
                    width: `${stabilityData?.overall_score ? stabilityData.overall_score * 100 : 0}%`,
                    backgroundColor: getStabilityColor(stabilityData).replace('text-', '#')
                  }}
                ></div>
              </div>
            </div>
            
            {/* Stability Factors */}
            {stabilityData?.factors && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold mb-3">Stability Factors</h3>
                <div className="grid grid-cols-2 gap-3">
                  {Object.entries(stabilityData.factors).map(([key, value]) => (
                    <div key={key} className="bg-gray-700 rounded p-3">
                      <div className="text-sm text-gray-400">{key}</div>
                      <div className="font-semibold">{(value * 100).toFixed(1)}%</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Crisis Timeline */}
          <div className="timeline-panel">
            <h2 className="text-xl font-bold mb-4">Crisis Timeline Feed</h2>
            <div className="timeline-list">
              {timelineEvents.length === 0 ? (
                <div className="text-gray-400 text-center py-8">
                  No events yet - waiting for system activity
                </div>
              ) : (
                timelineEvents.slice(-10).reverse().map((event, index) => (
                  <div key={index} className="timeline-event">
                    <div className={`event-indicator ${event.severity || 'info'}`}></div>
                    <div className="event-content">
                      <div className="event-title">{event.event_type}</div>
                      <div className="event-description">{event.description}</div>
                      <div className="event-time">{new Date(event.timestamp).toLocaleString()}</div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReliableCommandCenter;
