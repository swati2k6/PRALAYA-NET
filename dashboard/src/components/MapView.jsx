import { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, Circle, useMapEvents } from "react-leaflet";
import { fetchDisasterZones, getSystemStatus, getDroneStatus } from "../services/api";
import { fetchInfrastructureLayer } from "../services/geoIntelligenceService";
import RiskPopup from "./RiskPopup";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// Fix for default marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

const MapView = () => {
  const [zones, setZones] = useState([]);
  const [infrastructure, setInfrastructure] = useState([]);
  const [drones, setDrones] = useState([]);
  const [center] = useState([28.6139, 77.2090]);

  // Geo-Intelligence State
  const [activePopup, setActivePopup] = useState(null);
  const [showIntelLayer, setShowIntelLayer] = useState(false);
  const [intelMarkers, setIntelMarkers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [zonesData, statusData, droneData] = await Promise.all([
          fetchDisasterZones().catch(err => {
            console.error("Error fetching zones:", err);
            return { zones: [] };
          }),
          getSystemStatus().catch(err => {
            console.error("Error fetching status:", err);
            return { cascading_analysis: null };
          }),
          getDroneStatus().catch(err => {
            console.error("Error fetching drones:", err);
            return { drones: [] };
          })
        ]);

        setZones(zonesData.zones || []);

        if (statusData.cascading_analysis?.graph?.nodes) {
          setInfrastructure(statusData.cascading_analysis.graph.nodes);
        }

        setDrones(droneData.drones || []);
      } catch (error) {
        console.error("Error fetching map data:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  // Fetch Intel Layer when enabled
  useEffect(() => {
    if (showIntelLayer) {
      fetchInfrastructureLayer(center[0], center[1]).then(setIntelMarkers);
    } else {
      setIntelMarkers([]);
    }
  }, [showIntelLayer, center]);

  const MapEvents = () => {
    useMapEvents({
      click(e) {
        setActivePopup({
          lat: e.latlng.lat,
          lon: e.latlng.lng
        });
      },
    });
    return null;
  };

  const getDisasterColor = (type) => {
    const colors = {
      flood: "#4a90e2",
      fire: "#c45a5a",
      earthquake: "#d4a574",
      cyclone: "#8b7fa8",
      landslide: "#8a6f5a",
    };
    return colors[type] || "#6b7280";
  };

  const getRiskColor = (risk) => {
    if (risk >= 0.8) return "#b84a4a";
    if (risk >= 0.6) return "#c45a5a";
    if (risk >= 0.3) return "#d4a574";
    return "#5a8a5a";
  };

  return (
    <div className="map-container" style={{ position: 'relative' }}>
      <div className="map-header">
        <h2 className="map-title">Geospatial Situational Awareness</h2>
      </div>

      <div className="infrastructure-toggle">
        <span className="toggle-label">Infrastructure Intelligence</span>
        <input
          type="checkbox"
          checked={showIntelLayer}
          onChange={(e) => setShowIntelLayer(e.target.checked)}
        />
      </div>

      <MapContainer
        center={center}
        zoom={12}
        style={{ height: "100%", width: "100%" }}
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <MapEvents />

        {/* Global Geo-Intelligence Popup */}
        {activePopup && (
          <Popup position={[activePopup.lat, activePopup.lon]} onClose={() => setActivePopup(null)}>
            <RiskPopup lat={activePopup.lat} lon={activePopup.lon} />
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
              weight: 2,
            }}
          >
            <Popup>
              <div style={{ fontSize: '12px', fontFamily: 'Inter, sans-serif' }}>
                <strong>{zone.type?.toUpperCase()}</strong>
                <br />
                <span style={{ color: '#666' }}>Severity: {(zone.severity * 100).toFixed(0)}%</span>
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
              className: "infrastructure-marker",
              html: `<div style="
                background-color: ${getRiskColor(node.risk)};
                width: 16px;
                height: 16px;
                border-radius: 50%;
                border: 2px solid #1a1d29;
                box-shadow: 0 0 3px rgba(0,0,0,0.8);
              "></div>`,
              iconSize: [16, 16],
            })}
          >
            <Popup>
              <div style={{ fontSize: '12px', fontFamily: 'Inter, sans-serif' }}>
                <strong>{node.name}</strong>
                <br />
                <span style={{ color: '#666' }}>Type: {node.type}</span>
                <br />
                <span style={{ color: getRiskColor(node.risk), fontWeight: '600' }}>
                  Risk: {(node.risk * 100).toFixed(0)}% ({node.risk_level.toUpperCase()})
                </span>
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Intelligence Layer Markers */}
        {intelMarkers.map((marker) => (
          <Marker
            key={marker.id}
            position={[marker.lat, marker.lon]}
            icon={L.divIcon({
              className: "intel-marker",
              html: `<div style="
                background: #5a7aa5;
                width: 12px;
                height: 12px;
                transform: rotate(45deg);
                border: 1px solid white;
              "></div>`,
              iconSize: [12, 12],
            })}
          >
            <Popup>
              <div style={{ fontSize: '10px', fontWeight: 'bold' }}>
                INTEL: {marker.name}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Drone Positions */}
        {drones.map((drone) => {
          if (!drone.location) return null;

          return (
            <Marker
              key={drone.id}
              position={[drone.location.lat, drone.location.lon]}
              icon={L.divIcon({
                className: "drone-marker",
                html: `<div style="
                  width: 0;
                  height: 0;
                  border-left: 6px solid transparent;
                  border-right: 6px solid transparent;
                  border-bottom: 12px solid ${drone.slam_enabled ? '#d4a574' : '#4a90e2'};
                  transform: rotate(${drone.heading || 0}deg);
                "></div>`,
                iconSize: [12, 12],
              })}
            >
              <Popup>
                <div style={{ fontSize: '12px', fontFamily: 'Inter, sans-serif' }}>
                  <strong>{drone.id}</strong>
                  <br />
                  <span style={{ color: '#666' }}>
                    {drone.slam_enabled ? 'V-SLAM Mode' : 'GPS Navigation'}
                  </span>
                  <br />
                  <span style={{ color: '#666', fontSize: '10px' }}>
                    Alt: {drone.altitude?.toFixed(0)}m | Battery: {drone.battery?.toFixed(0)}%
                  </span>
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default MapView;
