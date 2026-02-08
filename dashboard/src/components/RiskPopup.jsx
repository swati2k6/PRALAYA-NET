import { useState, useEffect } from 'react'
import { fetchGeoIntel } from '../services/geoIntelligenceService'

const RiskPopup = ({ lat, lon, onClose }) => {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    const getIntelligence = async () => {
      setLoading(true)
      try {
        console.log('[RiskPopup] Fetching geo-intel for:', lat, lon)
        const geoData = await fetchGeoIntel(lat, lon)
        setData(geoData)
        setError(null)
      } catch (err) {
        console.error('[RiskPopup] Error:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    if (lat && lon) {
      getIntelligence()
    }
  }, [lat, lon])

  // Calculate high risk indicator
  const isHighRisk = data?.risk_score >= 70 || data?.risk_level === 'critical'

  const getBadgeColor = (score, level) => {
    if (level === 'critical' || score >= 80) return 'red'
    if (level === 'high' || score >= 60) return 'orange'
    if (level === 'elevated' || score >= 40) return 'orange'
    return 'green'
  }

  const badgeColor = data ? getBadgeColor(data.risk_score, data.risk_level) : 'green'

  if (loading) {
    return (
      <div className="risk-popup-loading">
        <div className="spinner"></div>
        <span>Analyzing Geo-Intelligence...</span>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="risk-popup-error" style={{ padding: '20px', textAlign: 'center' }}>
        <div style={{ fontSize: '24px', marginBottom: '10px' }}>⚠️</div>
        <div style={{ fontSize: '12px', color: '#c45a5a' }}>Service Unavailable</div>
        <div style={{ fontSize: '10px', color: '#8a8d94', marginTop: '5px' }}>
          Using demo data
        </div>
      </div>
    )
  }

  const weather = data.weather || {}
  const nasa = data.nasa_data || {}

  return (
    <div className="intel-card" style={{ minWidth: '240px' }}>
      {/* Header */}
      <div style={{ marginBottom: '12px' }}>
        <div style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '2px' }}>
          {weather.name || 'Regional Analysis'}
        </div>
        <div style={{ fontSize: '9px', color: '#8a8d94' }}>
          {data.coordinates?.lat?.toFixed(4)}, {data.coordinates?.lon?.toFixed(4)}
        </div>
      </div>

      {/* Risk Badge */}
      <div className={`intel-badge ${badgeColor}`}>
        AI RISK: {data.risk_level.toUpperCase()} ({data.risk_score}%)
      </div>

      {/* Weather Section */}
      <div className="intel-section" style={{ marginTop: '15px' }}>
        <div className="section-label">Atmospheric Intelligence</div>
        <div className="intel-grid">
          <div className="intel-item">
            <span className="label">Temperature</span>
            <span className="value">{weather.main?.temp?.toFixed(1) || '--'}°C</span>
          </div>
          <div className="intel-item">
            <span className="label">Wind Speed</span>
            <span className="value">{(weather.wind?.speed * 3.6).toFixed(1) || '--'} km/h</span>
          </div>
          <div className="intel-item">
            <span className="label">Humidity</span>
            <span className="value">{weather.main?.humidity || '--'}%</span>
          </div>
          <div className="intel-item">
            <span className="label">Condition</span>
            <span className="value">{weather.weather?.[0]?.description || '--'}</span>
          </div>
        </div>
      </div>

      {/* NASA Section */}
      <div className="intel-divider"></div>
      <div className="intel-section">
        <div className="section-label">NASA Environmental Monitoring</div>
        <div className="intel-grid">
          <div className="intel-item">
            <span className="label">SFC Temp</span>
            <span className="value">{nasa.temperature?.toFixed(1) || '--'}°C</span>
          </div>
          <div className="intel-item">
            <span className="label">Precipitation</span>
            <span className="value">{nasa.precipitation?.toFixed(2) || '--'} mm</span>
          </div>
        </div>
        {nasa.precipitation > 0.5 && (
          <div className="intel-anomaly">
            ⚠️ High Precipitation Anomaly Detected
          </div>
        )}
      </div>

      {/* Infrastructure */}
      {data.infrastructure && data.infrastructure.length > 0 && (
        <>
          <div className="intel-divider"></div>
          <div className="intel-section">
            <div className="section-label">Nearby Infrastructure</div>
            {data.infrastructure.slice(0, 3).map((facility) => (
              <div key={facility.id} style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                padding: '4px 0',
                fontSize: '10px',
                borderBottom: '1px solid #2f3240'
              }}>
                <span>{facility.name}</span>
                <span style={{ color: '#8a8d94' }}>{facility.distance_km} km</span>
              </div>
            ))}
          </div>
        </>
      )}

      {/* Footer */}
      <div style={{ 
        marginTop: '12px', 
        paddingTop: '8px', 
        borderTop: '1px solid #2f3240',
        fontSize: '8px',
        color: '#6b7280',
        textAlign: 'right'
      }}>
        Updated: {new Date(data.timestamp).toLocaleTimeString()}
      </div>
    </div>
  )
}

export default RiskPopup

