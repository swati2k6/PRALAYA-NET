import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import CommandCenter from './components/CommandCenter'
import EnhancedCommandCenter from './components/EnhancedCommandCenterFixed'
import ReliableCommandCenter from './components/ReliableCommandCenter'
import DemoCommandCenter from './components/DemoCommandCenter'
import ErrorBoundary from './components/ErrorBoundary'
import './index.css'

// Navigation component
const Navigation = () => {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [backendStatus, setBackendStatus] = useState('unknown')

  // Check backend status
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch('/api/health')
        setBackendStatus(response.ok ? 'online' : 'offline')
      } catch {
        setBackendStatus('offline')
      }
    }
    
    checkBackend()
    const interval = setInterval(checkBackend, 10000)
    return () => clearInterval(interval)
  }, [])

  const navLinks = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/command-center', label: 'Command Center', icon: '🎛️' },
    { path: '/enhanced-command-center', label: 'Enhanced CC', icon: '⚡' },
    { path: '/demo-command-center', label: 'Demo CC', icon: '🎯' }
  ]

  const isActive = (path) => location.pathname === path

  return (
    <nav style={{
      background: 'linear-gradient(180deg, #1a1d29 0%, #232633 100%)',
      borderBottom: '1px solid #3a3d4a',
      position: 'sticky',
      top: 0,
      zIndex: 1000
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '0 20px'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          height: '64px'
        }}>
          {/* Logo */}
          <Link to="/" style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            textDecoration: 'none',
            color: '#e8e9ea'
          }}>
            <span style={{ fontSize: '24px' }}>🚀</span>
            <div>
              <div style={{
                fontSize: '16px',
                fontWeight: '700',
                letterSpacing: '1px',
                background: 'linear-gradient(90deg, #4a90e2, #c45a5a)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }}>
                PRALAYA-NET
              </div>
              <div style={{
                fontSize: '8px',
                color: '#8a8d94',
                textTransform: 'uppercase',
                letterSpacing: '2px'
              }}>
                Disaster Command System
              </div>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '8px 16px',
                  borderRadius: '6px',
                  textDecoration: 'none',
                  fontSize: '13px',
                  fontWeight: '500',
                  color: isActive(link.path) ? '#e8e9ea' : '#8a8d94',
                  background: isActive(link.path) ? 'rgba(74, 144, 226, 0.15)' : 'transparent',
                  border: isActive(link.path) ? '1px solid rgba(74, 144, 226, 0.3)' : '1px solid transparent',
                  transition: 'all 0.2s ease'
                }}
              >
                <span>{link.icon}</span>
                <span className="nav-label">{link.label}</span>
              </Link>
            ))}
          </div>

          {/* Status & Mobile Menu */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '16px'
          }}>
            {/* Backend Status */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '6px 12px',
              background: 'rgba(0,0,0,0.2)',
              borderRadius: '20px',
              fontSize: '11px'
            }}>
              <span style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                background: backendStatus === 'online' ? '#5a8a5a' : backendStatus === 'offline' ? '#c45a5a' : '#d4a574',
                animation: backendStatus === 'online' ? 'pulse 2s infinite' : 'none'
              }}></span>
              <span style={{ color: '#8a8d94' }}>
                {backendStatus === 'online' ? 'Backend Online' : backendStatus === 'offline' ? 'Offline' : 'Checking...'}
              </span>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              style={{
                display: 'none',
                flexDirection: 'column',
                gap: '4px',
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '8px',
                color: '#e8e9ea'
              }}
              className="mobile-menu-btn"
            >
              <span style={{
                width: '20px',
                height: '2px',
                background: 'currentColor',
                borderRadius: '2px',
                transition: 'all 0.3s ease'
              }}></span>
              <span style={{
                width: '20px',
                height: '2px',
                background: 'currentColor',
                borderRadius: '2px',
                transition: 'all 0.3s ease'
              }}></span>
              <span style={{
                width: '20px',
                height: '2px',
                background: 'currentColor',
                borderRadius: '2px',
                transition: 'all 0.3s ease'
              }}></span>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            padding: '16px 0',
            borderTop: '1px solid #3a3d4a'
          }}>
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  padding: '12px 16px',
                  borderRadius: '6px',
                  textDecoration: 'none',
                  fontSize: '14px',
                  fontWeight: '500',
                  color: isActive(link.path) ? '#e8e9ea' : '#8a8d94',
                  background: isActive(link.path) ? 'rgba(74, 144, 226, 0.15)' : 'transparent'
                }}
              >
                <span>{link.icon}</span>
                <span>{link.label}</span>
              </Link>
            ))}
          </div>
        )}
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        @media (max-width: 768px) {
          .mobile-menu-btn { display: flex !important; }
          .nav-label { display: none !important; }
        }
        @media (min-width: 769px) {
          .mobile-menu-btn { display: none !important; }
        }
      `}</style>
    </nav>
  )
}

function App() {
  return (
    <Router>
      <ErrorBoundary>
        <div style={{
          minHeight: '100vh',
          background: '#1a1d29',
          fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
        }}>
          <Navigation />
          
          <main style={{
            flex: 1,
            background: '#1a1d29'
          }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/command-center" element={<CommandCenter />} />
              <Route path="/enhanced-command-center" element={<EnhancedCommandCenter />} />
              <Route path="/reliable-command-center" element={<ReliableCommandCenter />} />
              <Route path="/demo-command-center" element={<DemoCommandCenter />} />
            </Routes>
          </main>

          {/* Footer */}
          <footer style={{
            padding: '16px 20px',
            background: '#232633',
            borderTop: '1px solid #3a3d4a',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '12px'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '20px',
              fontSize: '12px',
              color: '#8a8d94'
            }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#5a8a5a' }}></span>
                System Operational
              </span>
              <span>NDMA Compatible</span>
              <span>ISRO Integrated</span>
            </div>
            <div style={{
              fontSize: '11px',
              color: '#6b7280'
            }}>
              © 2024 PRALAYA-NET | v1.0.0
            </div>
          </footer>
        </div>
      </ErrorBoundary>
    </Router>
  )
}

export default App

