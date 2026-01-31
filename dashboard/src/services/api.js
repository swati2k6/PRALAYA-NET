// dashboard/src/services/api.js

const API_BASE = "";

// Helper function for API calls with error handling
async function apiCall(url, options = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: response.statusText }));
      throw new Error(errorData.error || errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    if (error.message.includes("Failed to fetch") || error.message.includes("NetworkError")) {
      throw new Error("Cannot connect to backend server. Please ensure the backend is running on http://127.0.0.1:8000");
    }
    throw error;
  }
}

// Trigger disaster
export async function triggerDisaster(disasterType, severity = 0.7, location = null) {
  return apiCall(`${API_BASE}/api/trigger/disaster`, {
    method: "POST",
    body: JSON.stringify({
      disaster_type: disasterType,
      severity: severity,
      location: location,
    }),
  });
}

// Get satellite zones
export async function fetchDisasterZones() {
  return apiCall(`${API_BASE}/api/satellite/zones`);
}

// Get cascading risk graph
export async function getRiskGraph() {
  return apiCall(`${API_BASE}/api/trigger/status`);
}

// Get drone status
export async function getDroneStatus() {
  return apiCall(`${API_BASE}/api/drones/status`);
}

// Get drone telemetry
export async function getDroneTelemetry(droneId) {
  return apiCall(`${API_BASE}/api/drones/telemetry/${droneId}`);
}

// Deploy drone
export async function deployDrone(location) {
  return apiCall(`${API_BASE}/api/drones/deploy`, {
    method: "POST",
    body: JSON.stringify(location),
  });
}

// Clear all disasters
export async function clearDisasters() {
  return apiCall(`${API_BASE}/api/trigger/clear`, {
    method: "POST",
  });
}

// Get system status
export async function getSystemStatus() {
  return apiCall(`${API_BASE}/api/trigger/status`);
}
