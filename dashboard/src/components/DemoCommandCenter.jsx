import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { API_ENDPOINTS, WS_ENDPOINTS, CONFIG } from '../config/demo_api';
import '../styles/CommandCenter.css';

// Fix leaflet default icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const DemoCommandCenter = () => {
  const [systemData, setSystemData] = useState(null);
  const [stabilityData, setStabilityData] = useState(null);
  const [riskData, setRiskData] = useState(null);
  const [activeAlerts, setActiveAlerts] = useState([]);
  const [timelineEvents, setTimelineEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [demoMode, setDemoMode] = useState(true);
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

  // Mock data generators for fallback
  const generateMockData = () => {
    const mockRisk = {
      risk_score: Math.random() * 0.8 + 0.1,
      risk_level: ['low', 'medium', 'high', 'critical'][Math.floor(Math.random() * 4)],
      confidence: Math.random() * 0.3 + 0.7,
      factors: {
        rainfall_weight: Math.random() * 0.3 + 0.1,
        earthquake_weight: Math.random() * 0.3,
        infrastructure_weight: Math.random() * 0.3 + 0.2,
        historical_weight: Math.random() * 0.1 + 0.05
      },
      timestamp: new Date().toISOString()
    };

    const mockStability = {
      overall_score: Math.random() * 0.4 + 0.6,
      level: ['excellent', 'healthy', 'warning'][Math.floor(Math.random() * 3)],
      factors: {
        infrastructure_health: Math.random() * 0.3 + 0.6,
        disaster_risk: Math.random() * 0.3 + 0.2,
        agent_response_capacity: Math.random() * 0.3 + 0.7,
        temporal_stability: Math.random() * 0.4 + 0.4
      },
      trend: ['improving', 'stable', 'declining'][Math.floor(Math.random() * 3)],
      timestamp: new Date().toISOString()
    };

    const mockAlerts = Array.from({ length: Math.floor(Math.random() * 4) + 2 }, (_, i) => ({
      alert_id: `alert_${i}_${Date.now()}`,
      alert_type: ['infrastructure_monitoring', 'risk_assessment', 'system_check'][Math.floor(Math.random() * 3)],
      severity: ['info', 'warning', 'critical'][Math.floor(Math.random() * 3)],
      description: `Autonomous monitoring in progress`,
      location: ['Mumbai', 'Delhi', 'Chennai', 'Kolkata'][Math.floor(Math.random() * 4)],
      progress: Math.random() * 0.7 + 0.2,
      timestamp: new Date(Date.now() - Math.random() * 3600000).toISOString()
    }));

    const mockEvents = Array.from({ length: Math.floor(Math.random() * 6) + 4 }, (_, i) => ({
      event_id: `event_${i}`,
      event_type: ['system_check', 'agent_update', 'risk_assessment'][Math.floor(Math.random() * 3)],
      description: `System performing autonomous monitoring`,
      severity: ['info', 'warning', 'critical'][Math.floor(Math.random() * 3)],
      location: ['National', 'Mumbai', 'Delhi'][Math.floor(Math.random() * 3)],
      timestamp: new Date(Date.now() - Math.random() * 7200000).toISOString()
    }));

    return { mockRisk, mockStability, mockAlerts, mockEvents };
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
        // Automatically switch to demo mode if backend unreachable
        if (!demoMode) {
          console.log('Backend unreachable - switching to demo mode');
          setDemoMode(true);
          const { mockRisk, mockStability, mockAlerts, mockEvents } = generateMockData();
          setRiskData(mockRisk);
          setStabilityData(mockStability);
          setActiveAlerts(mockAlerts);
          setTimelineEvents(mockEvents);
        }
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
  }, [demoMode]);

  // Auto-refresh data every 5 seconds
  useEffect(() => {
    const refreshInterval = setInterval(async () => {
      if (backendStatus === 'online') {
        await refreshData();
      } else {
        // Refresh mock data in demo mode
        const { mockRisk, mockStability, mockAlerts, mockEvents } = generateMockData();
        setRiskData(mockRisk);
        setStabilityData(mockStability);
        setActiveAlerts(mockAlerts);
        setTimelineEvents(mockEvents);
      }
    }, CONFIG.UPDATE_INTERVAL);

    return () => clearInterval(refreshInterval);
  }, [backendStatus]);

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
        setStabilityData(data.data.stability_index);
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
        setActiveAlerts(prev => [...prev.slice(-9), data.data]);
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
        setRiskData(data.data);
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
      const systemResponse = await fetch(API_ENDPOINTS.DEMO_STATUS);
      const systemData = await systemResponse.json();
      setSystemData(systemData);

      // Fetch stability data
      const stabilityResponse = await fetch(API_ENDPOINTS.STABILITY_CURRENT);
      const stabilityData = await stabilityResponse.json();
      setStabilityData(stabilityData.stability_index);

      // Fetch risk data
      const riskResponse = await fetch(API_ENDPOINTS.RISK_PREDICT);
      const riskData = await riskResponse.json();
      setRiskData(riskData);

      // Fetch alerts
      const alertsResponse = await fetch(API_ENDPOINTS.ALERTS_ACTIVE);
      const alertsData = await alertsResponse.json();
      setActiveAlerts(alertsData.alerts);

      // Fetch timeline events
      const timelineResponse = await fetch(API_ENDPOINTS.TIMELINE_EVENTS);
      const timelineData = await timelineResponse.json();
      setTimelineEvents(timelineData.events);

      setBackendStatus('online');
      console.log('✅ Connected to PRALAYA-NET backend');
      setLoading(false);
    } catch (error) {
      console.error('❌ Error connecting to backend:', error);
      setBackendStatus('offline');
      setDemoMode(true);
      
      // Automatically use mock data
      const { mockRisk, mockStability, mockAlerts, mockEvents } = generateMockData();
      setRiskData(mockRisk);
      setStabilityData(mockStability);
      setActiveAlerts(mockAlerts);
      setTimelineEvents(mockEvents);
      
      setLoading(false);
    }
  };

  const refreshData = async () => {
    try {
      // Refresh stability data
      const stabilityResponse = await fetch(API_ENDPOINTS.STABILITY_CURRENT);
      const stabilityData = await stabilityResponse.json();
      setStabilityData(stabilityData.stability_index);

      // Refresh risk data
      const riskResponse = await fetch(API_ENDPOINTS.RISK_PREDICT);
      const riskData = await riskResponse.json();
      setRiskData(riskData);

      // Refresh alerts
      const alertsResponse = await fetch(API_ENDPOINTS.ALERTS_ACTIVE);
      const alertsData = await alertsResponse.json();
      setActiveAlerts(alertsData.alerts);

      // Refresh timeline events
      const timelineResponse = await fetch(API_ENDPOINTS.TIMELINE_EVENTS);
      const timelineData = await timelineResponse.json();
      setTimelineEvents(timelineData.events);
    } catch (error) {
      console.error('Error refreshing data:', error);
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
             'Backend offline - using demo mode'}
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
                       backendStatus === 'offline' ? '🔴 Offline (Demo Mode)' : 
                       '🟡 Checking...'}
              </span>
            </div>
            {demoMode && (
              <div className="flex items-center space-x-2 bg-yellow-900 px-3 py-1 rounded">
                <span className="text-yellow-300 text-sm">🎯 Demo Mode Active</span>
              </div>
            )}
          </div>
        </div>
        <p className="text-gray-400">Emergency Production Autonomous Disaster-Response Platform</p>
      </header>

      {/* Main Grid Layout */}
      <div className="command-grid">
        {/* Left Panel - Command Controls */}
        <div className="command-panel">
          <h2 className="text-2xl font-bold mb-4">Command Controls</h2>
          
          <div className="control-buttons">
            <button
              onClick={() => setDemoMode(!demoMode)}
              className={`control-btn ${demoMode ? 'active' : ''}`}
            >
              {demoMode ? '🎯 Demo Mode' : '🔗 Live Mode'}
            </button>
            <button
              onClick={refreshData}
              className="control-btn"
            >
              🔄 Refresh Data
            </button>
          </div>

          <div className="control-buttons">
            <button
              onClick={simulateDisaster}
              className="control-btn danger"
            >
              🚨 Simulate Disaster
            </button>
          </div>

          {/* Active Alerts */}
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-3">Active Alerts ({activeAlerts.length})</h3>
            <div className="action-list">
              {activeAlerts.length === 0 ? (
                <div className="text-gray-400 text-center py-8">
                  No active alerts - System monitoring
                </div>
              ) : (
                activeAlerts.slice(0, 5).map((alert, index) => (
                  <div key={index} className="action-item">
                    <div className="action-header">
                      <span className="action-title">{alert.alert_type}</span>
                      <span className={`action-status ${alert.severity}`}>{alert.severity}</span>
                    </div>
                    <div className="action-description text-sm text-gray-400 mb-2">
                      {alert.description} - {alert.location}
                    </div>
                    <div className="action-progress">
                      <div 
                        className="action-progress-fill" 
                        style={{ width: `${alert.progress || 0}%` }}
                      ></div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Center Panel - Live Map */}
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
              
              {/* Sample infrastructure nodes with current risk */}
              <CircleMarker
                center={[19.0760, 72.8777]} // Mumbai
                radius={50000}
                fillColor={getRiskColor(riskData?.risk_score || 0.5)}
                color={getRiskColor(riskData?.risk_score || 0.5)}
                weight={2}
                opacity={0.6}
              >
                <Popup>
                  <div className="text-sm">
                    <strong>Mumbai Infrastructure</strong><br/>
                    Risk: {riskData?.risk_level || 'Medium'}<br/>
                    Score: {riskData?.risk_score ? (riskData.risk_score * 100).toFixed(1) : '50'}%<br/>
                    Status: Active Monitoring
                  </div>
                </Popup>
              </CircleMarker>
              
              <CircleMarker
                center={[28.7041, 77.1025]} // Delhi
                radius={40000}
                fillColor={getRiskColor((riskData?.risk_score || 0.5) * 0.8)}
                color={getRiskColor((riskData?.risk_score || 0.5) * 0.8)}
                weight={2}
                opacity={0.6}
              >
                <Popup>
                  <div className="text-sm">
                    <strong>Delhi Infrastructure</strong><br/>
                    Risk: {riskData?.risk_level || 'Medium'}<br/>
                    Score: {riskData?.risk_score ? (riskData.risk_score * 80).toFixed(1) : '40'}%<br/>
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
                timelineEvents.slice(-8).reverse().map((event, index) => (
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

export default DemoCommandCenter;
