import { useState, useEffect } from "react"
import MapView from "../components/MapView"
import ControlPanel from "../components/ControlPanel"
import StatusPanel from "../components/StatusPanel"
import IntelligenceFeed from "../components/IntelligenceFeed"
import { checkBackendHealth, fetchSystemStatus, fetchStabilityIndex } from "../services/api"
import "../index.css"

// Mock data generators for fallback when backend offline
const generateMockStabilityData = () => ({
  stability_index: {
    overall_score: Math.random() * 0.4 + 0.6,
    level: "healthy",
    factors: {
      infrastructure_health: Math.random() * 0.4 + 0.6,
      disaster_risk: Math.random() * 0.4 + 0.2,
      agent_response_capacity: Math.random() * 0.4 + 0.7,
      temporal_stability: Math.random() * 0.4 + 0.4
    },
    trend: "stable",
    timestamp: new Date().toISOString()
  }
})

const generateMockAlerts = () => [
  {
    alert_id: `alert_${Date.now()}`,
    alert_type: "system_check",
    severity: "info",
    description: "Demo mode active - mock data",
    location: "System",
    progress: 1.0,
    timestamp: new Date().toISOString()
  }
]

const generateMockTimeline = () => [
  {
    event_id: `event_${Date.now()}`,
    event_type: "system_check",
    description: "System operating in demo mode",
    severity: "info",
    location: "Global",
    timestamp: new Date().toISOString()
  }
]

const Dashboard = () => {
  const [systemStatus, setSystemStatus] = useState(null)
  const [backendOnline, setBackendOnline] = useState(false)
  const [connectionError, setConnectionError] = useState(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [mobileRightPanelOpen, setMobileRightPanelOpen] = useState(false)
  const [apiUrl, setApiUrl] = useState('http://127.0.0.1:8000')

  // Initialize API URL from environment
  useEffect(() => {
    // Try to get from environment
    const envUrl = import.meta.env.VITE_API_URL || import.meta.env.NEXT_PUBLIC_API_URL
    if (envUrl) {
      setApiUrl(envUrl)
      console.log('[Dashboard] Using API URL from env:', envUrl)
    }
  }, [])

  // Close mobile menu when screen resizes to tablet+
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setMobileMenuOpen(false)
        setMobileRightPanelOpen(false)
      }
    }

    window.addEventListener("resize", handleResize)
    return () => window.removeEventListener("resize", handleResize)
  }, [])

  // Check backend health on mount
  useEffect(() => {
    const initBackend = async () => {
      try {
        console.log('[Dashboard] Checking backend health...')
        const isHealthy = await checkBackendHealth()
        setBackendOnline(isHealthy)

        if (!isHealthy) {
          setConnectionError("Backend offline - using demo mode")
          console.warn("[Dashboard] Backend is not responding, using demo data")
        } else {
          setConnectionError(null)
          console.log("[Dashboard] Backend is online")
        }
      } catch (error) {
        console.error("[Dashboard] Failed to initialize backend:", error)
        setBackendOnline(false)
        setConnectionError(error.message)
      }
    }

    initBackend()

    // Check backend health every 30 seconds
    const healthCheckInterval = setInterval(initBackend, 30000)
    return () => clearInterval(healthCheckInterval)
  }, [])

  // Fetch system status when backend is online
  useEffect(() => {
    if (!backendOnline) return

    const fetchStatus = async () => {
      try {
        const data = await fetchSystemStatus()
        setSystemStatus(data)
        setConnectionError(null)
      } catch (error) {
        console.error("[Dashboard] Error fetching system status:", error.message)
        setBackendOnline(false)
        setConnectionError("Failed to fetch system status")
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 10000) // Polling as backup every 10s
    return () => clearInterval(interval)
  }, [backendOnline])

  // Automatic refresh every 5 seconds for stability index, alerts, and timeline
  useEffect(() => {
    const refreshInterval = setInterval(async () => {
      if (!backendOnline) {
        // Use mock data when backend offline
        setSystemStatus({
          stability_index: generateMockStabilityData().stability_index,
          alerts: generateMockAlerts(),
          timeline: generateMockTimeline(),
          demo_mode: true
        })
      } else {
        // Fetch real data when backend online
        try {
          const data = await fetchSystemStatus()
          setSystemStatus(data)
        } catch (error) {
          console.error("[Dashboard] Refresh error:", error)
          setBackendOnline(false)
        }
      }
    }, 5000) // 5 seconds

    return () => clearInterval(refreshInterval)
  }, [backendOnline])

  return (
    <div className="command-center">
      <header className="command-header">
        <div className="header-left">
          <h1 className="system-title">PRALAYA-NET</h1>
          <span className="system-subtitle">Unified Disaster Command System</span>
        </div>

        <div className="header-right">
          {/* Connection Status */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontSize: '11px'
          }}>
            <span style={{
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              backgroundColor: backendOnline ? '#00ff00' : '#ff4444',
              display: 'inline-block'
            }}></span>
            <span className="backend-label">Backend:</span>
            {backendOnline ? "ONLINE" : "OFFLINE"}
          </div>
          
          <div className="mode-indicator">
            <span className="mode-label">MODE</span>
            <span className="mode-status">{backendOnline ? "LIVE DATA" : "SIMULATION"}</span>
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

          {/* Mobile Menu Buttons */}
          <button
            className={`mobile-menu-btn ${mobileMenuOpen ? "active" : ""}`}
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle left panel"
            title="Control Panel"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>

          <button
            className={`mobile-menu-btn ${mobileRightPanelOpen ? "active" : ""}`}
            onClick={() => setMobileRightPanelOpen(!mobileRightPanelOpen)}
            aria-label="Toggle right panel"
            title="Intelligence Feed"
            style={{ marginRight: "-8px" }}
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </header>

      {/* Mobile Overlay */}
      {(mobileMenuOpen || mobileRightPanelOpen) && (
        <div
          className="mobile-overlay active"
          onClick={() => {
            setMobileMenuOpen(false)
            setMobileRightPanelOpen(false)
          }}
        />
      )}

      {/* Connection Error Banner */}
      {connectionError && !backendOnline && (
        <div style={{
          padding: '8px 20px',
          background: 'rgba(196, 90, 90, 0.2)',
          borderBottom: '1px solid rgba(196, 90, 90, 0.3)',
          fontSize: '12px',
          color: '#c45a5a',
          textAlign: 'center'
        }}>
          ⚠️ {connectionError} - Running in demo mode with simulated data
        </div>
      )}

      <div className="command-grid">
        {/* LEFT PANEL - Control & Status */}
        <aside className={`panel-left ${mobileMenuOpen ? "mobile-open" : ""}`}>
          <ControlPanel />
          <StatusPanel systemStatus={systemStatus} />
        </aside>

        {/* CENTER PANEL - Geospatial Map */}
        <main className="panel-center">
          <MapView apiUrl={apiUrl} />
        </main>

        {/* RIGHT PANEL - Intelligence Feed */}
        <aside className={`panel-right ${mobileRightPanelOpen ? "mobile-open" : ""}`}>
          <IntelligenceFeed systemStatus={systemStatus} />
        </aside>
      </div>

      <footer className="command-footer">
        <div className="footer-left">
          <span>System Status: {backendOnline ? "OPERATIONAL" : "DEMO MODE"}</span>
          <span className="footer-separator">|</span>
          <span>Version 1.0.0</span>
        </div>
        <div className="footer-right">
          <span style={{ fontSize: "11px" }}>NDMA / ISRO Compatible Architecture</span>
        </div>
      </footer>

      <style>{`
        .backend-label {
          display: none;
        }
        @media (min-width: 640px) {
          .backend-label {
            display: inline;
          }
        }
      `}</style>
    </div>
  )
}

export default Dashboard

