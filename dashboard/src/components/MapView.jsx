import { useEffect, useState, useRef } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Circle, useMapEvents } from 'react-leaflet'
import { fetchGeoIntel, fetchInfrastructureLayer } from '../services/geoIntelligenceService'
import RiskPopup from './RiskPopup'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix for default marker icon
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

const MapView = ({ apiUrl = 'http://127.0.0.1:8000' }) => {
  const [zones, setZones] = useState([])
  const [infrastructure, setInfrastructure] = useState([])
  const [center] = useState([28.6139, 77.2090]) // Delhi, India
  const [activePopup, setActivePopup] = useState(null)
  const [showIntelLayer, setShowIntelLayer] = useState(false)
  const [intelMarkers, setIntelMarkers] = useState([])
  const [mapReady, setMapReady] = useState(false)
  const mapRef = useRef(null)

  // Map click handler
  const MapEvents = () => {
    useMapEvents({
      click(e) {
        const { lat, lng } = e.latlng
        console.log('[MapView] Map clicked at:', lat, lng)
        setActivePopup({
          lat,
          lon: lng,
          source: 'map_click'
        })
      },
      load() {
        setMapReady(true)
        console.log('[MapView] Map loaded')
      }
    })
    return null
  }

  // Fetch disaster zones
  const fetchZones = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/satellite/zones`)
      if (response.ok) {
        const data = await response.json()
        setZones(data.zones || [])
      }
    } catch (error) {
      console.error('[MapView] Error fetching zones:', error)
    }
  }

  // Fetch infrastructure
  const fetchInfra = async () => {
    try {
      const data = await fetchInfrastructureLayer(center[0], center[1])
      setInfrastructure(data)
    } catch (error) {
      console.error('[MapView] Error fetching infrastructure:', error)
    }
  }

  // Fetch intel layer when enabled
  const fetchIntel = async () => {
    if (!showIntelLayer) {
      setIntelMarkers([])
      return
    }
    
    try {
      const data = await fetchGeoIntel(center[0], center[1])
      if (data.infrastructure) {
        setIntelMarkers(data.infrastructure)
      }
    } catch (error) {
      console.error('[MapView] Error fetching intel:', error)
    }
  }

  // Initial data fetch
  useEffect(() => {
    fetchZones()
    fetchInfra()
    
    // Refresh every 30 seconds
    const interval = setInterval(() => {
      fetchZones()
      if (showIntelLayer) fetchIntel()
    }, 30000)
    
    return () => clearInterval(interval)
  }, [center, showIntelLayer])

  // Fetch intel when toggle changes
  useEffect(() => {
    fetchIntel()
  }, [showIntelLayer, center])

  // Get disaster color
  const getDisasterColor = (type) => {
    const colors = {
      flood: '#4a90e2',
      fire: '#c45a5a',
      earthquake: '#d4a574',
      cyclone: '#8b7fa8',
      landslide: '#8a6f5a'
    }
    return colors[type] || '#6b7280'
  }

  // Get risk color
  const getRiskColor = (risk) => {
    if (risk >= 0.8) return '#b84a4a'
    if (risk >= 0.6) return '#c45a5a'
    if (risk >= 0.3) return '#d4a574'
    return '#5a8a5a'
  }

  return (
    <div className="map-container" style={{ position: 'relative', height: '100%', width: '100%' }}>
      {/* Map Header */}
      <div className="map-header">
        <h2 className="map-title">🗺️ Geospatial Situational Awareness</h2>
      </div>

      {/* Intel Toggle */}
      <div className="infrastructure-toggle">
        <label className="toggle-label" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <input
            type="checkbox"
            checked={showIntelLayer}
            onChange={(e) => setShowIntelLayer(e.target.checked)}
            style={{ width: '16px', height: '16px', cursor: 'pointer' }}
          />
          <span>Infrastructure Intelligence</span>
        </label>
      </div>

      {/* Map Container */}
      <MapContainer
        ref={mapRef}
        center={center}
        zoom={12}
        style={{ height: '100%', width: '100%' }}
        zoomControl={true}
        whenReady={() => setMapReady(true)}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <MapEvents />

        {/* Click Popup - Shows Geo-Intel */}
        {activePopup && (
          <Popup
            position={[activePopup.lat, activePopup.lon]}
            onClose={() => setActivePopup(null)}
            maxWidth={300}
          >
            <RiskPopup
              lat={activePopup.lat}
              lon={activePopup.lon}
              onClose={() => setActivePopup(null)}
            />
          </Popup>
        )}

        {/* Disaster Zones */}
        {zones.map((zone) => (
          <Circle
            key={zone.id}
            center={[zone.location?.lat || center[0], zone.location?.lon || center[1]]}
            radius={zone.radius || 2000}
            pathOptions={{
              color: getDisasterColor(zone.type),
              fillColor: getDisasterColor(zone.type),
              fillOpacity: 0.25,
              weight: 2
            }}
          >
            <Popup>
              <div style={{ fontSize: '12px', fontFamily: 'Inter, sans-serif' }}>
                <strong>{zone.type?.toUpperCase()}</strong>
                <br />
                <span style={{ color: '#666' }}>
                  Severity: {(zone.severity * 100).toFixed(0)}%
                </span>
                <br />
                <span style={{ color: '#666', fontSize: '10px' }}>
                  {new Date(zone.detected_at).toLocaleString()}
                </span>
              </div>
            </Popup>
          </Circle>
        ))}

        {/* Infrastructure Nodes */}
        {infrastructure.map((node) => (
          <Marker
            key={node.id}
            position={[node.lat, node.lon]}
            icon={L.divIcon({
              className: 'infrastructure-marker',
              html: `<div style="
                background-color: ${getRiskColor(node.risk || 0.3)};
                width: 16px;
                height: 16px;
                border-radius: 50%;
                border: 2px solid #1a1d29;
                box-shadow: 0 0 3px rgba(0,0,0,0.8);
              "></div>`,
              iconSize: [16, 16]
            })}
          >
            <Popup>
              <div style={{ fontSize: '12px', fontFamily: 'Inter, sans-serif' }}>
                <strong>{node.name}</strong>
                <br />
                <span style={{ color: '#666' }}>Type: {node.type}</span>
                <br />
                <span style={{ color: getRiskColor(node.risk || 0.3), fontWeight: '600' }}>
                  Risk: {((node.risk || 0.3) * 100).toFixed(0)}%
                </span>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Intel Layer Markers */}
        {intelMarkers.map((marker) => (
          <Marker
            key={marker.id}
            position={[marker.lat, marker.lon]}
            icon={L.divIcon({
              className: 'intel-marker',
              html: `<div style="
                background: #5a7aa5;
                width: 12px;
                height: 12px;
                transform: rotate(45deg);
                border: 1px solid white;
              "></div>`,
              iconSize: [12, 12]
            })}
          >
            <Popup>
              <div style={{ fontSize: '10px', fontWeight: 'bold' }}>
                INTEL: {marker.name}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Center Marker */}
        <Marker position={center} icon={L.divIcon({
          className: 'center-marker',
          html: `<div style="
            background: transparent;
            width: 20px;
            height: 20px;
            border: 2px dashed #4a90e2;
            border-radius: 50%;
            animation: pulse 2s infinite;
          "></div>`,
          iconSize: [20, 20]
        })}>
          <Popup>
            <div style={{ fontSize: '12px', textAlign: 'center' }}>
              <strong>📍 Command Center</strong>
              <br />
              <span style={{ color: '#666' }}>Delhi, India</span>
              <br />
              <span style={{ fontSize: '10px', color: '#4a90e2' }}>
                Click anywhere for geo-intel
              </span>
            </div>
          </Popup>
        </Marker>
      </MapContainer>

      {/* Loading Overlay */}
      {!mapReady && (
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(26, 29, 41, 0.9)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000
        }}>
          <div style={{ textAlign: 'center' }}>
            <div className="spinner" style={{
              width: '40px',
              height: '40px',
              border: '4px solid rgba(74, 144, 226, 0.2)',
              borderTopColor: '#4a90e2',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              margin: '0 auto 15px'
            }}></div>
            <div style={{ color: '#e8e9ea', fontSize: '14px' }}>
              Loading Map...
            </div>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div style={{
        position: 'absolute',
        bottom: '60px',
        left: '12px',
        zIndex: 1000,
        background: 'rgba(26, 29, 41, 0.9)',
        border: '1px solid #3a3d4a',
        padding: '10px 14px',
        borderRadius: '4px',
        fontSize: '11px',
        color: '#b4b6ba',
        maxWidth: '250px'
      }}>
        <div style={{ fontWeight: '600', color: '#e8e9ea', marginBottom: '4px' }}>
          🖱️ Click anywhere on the map
        </div>
        <div>Get real-time weather, climate, and risk analysis for that location.</div>
      </div>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.2); opacity: 0.7; }
        }
      `}</style>
    </div>
  )
}

export default MapView

