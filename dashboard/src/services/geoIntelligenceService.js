/**
 * Geo-Intelligence Service for PRALAYA-NET Frontend
 * Uses backend proxy for weather, NASA, and infrastructure data
 */

import { API_BASE } from '../config/api'

const CACHE_TTL = 5 * 60 * 1000 // 5 minute cache
const cache = new Map()

/**
 * Fetch current weather via backend proxy
 */
export async function fetchCurrentWeather(lat, lon) {
  const cacheKey = `weather_${lat.toFixed(3)}_${lon.toFixed(3)}`
  
  // Check cache first
  if (cache.has(cacheKey)) {
    const cached = cache.get(cacheKey)
    if (Date.now() - cached.timestamp < CACHE_TTL) {
      console.log('[GeoIntel] Using cached weather data')
      return cached.data
    }
  }
  
  try {
    console.log('[GeoIntel] Fetching weather via backend:', lat, lon)
    const url = `${API_BASE}/api/weather?lat=${lat}&lon=${lon}`
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`Weather API failed: ${response.status}`)
    }
    
    const data = await response.json()
    
    // Cache the result
    cache.set(cacheKey, { data, timestamp: Date.now() })
    
    return data
  } catch (error) {
    console.error('[GeoIntel] Weather fetch error:', error)
    // Return simulated data as fallback
    return getSimulatedWeather(lat, lon)
  }
}

/**
 * Fetch climate data from NASA POWER via backend proxy
 */
export async function fetchNasaPower(lat, lon) {
  const cacheKey = `nasa_${lat.toFixed(3)}_${lon.toFixed(3)}`
  
  if (cache.has(cacheKey)) {
    const cached = cache.get(cacheKey)
    if (Date.now() - cached.timestamp < CACHE_TTL) {
      console.log('[GeoIntel] Using cached NASA data')
      return cached.data
    }
  }
  
  try {
    console.log('[GeoIntel] Fetching NASA data via backend:', lat, lon)
    // Use geo-intel endpoint which combines NASA data
    const url = `${API_BASE}/api/geo-intel?lat=${lat}&lon=${lon}`
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`NASA API failed: ${response.status}`)
    }
    
    const data = await response.json()
    
    // Cache the relevant NASA data
    const nasaResult = {
      temp: data.nasa_data?.temperature,
      precipitation: data.nasa_data?.precipitation,
      solar_radiation: data.nasa_data?.solar_radiation,
      relative_humidity: data.nasa_data?.relative_humidity
    }
    
    cache.set(cacheKey, { data: nasaResult, timestamp: Date.now() })
    
    return nasaResult
  } catch (error) {
    console.error('[GeoIntel] NASA fetch error:', error)
    return getSimulatedNasaData(lat, lon)
  }
}

/**
 * Fetch comprehensive geo-intelligence data
 */
export async function fetchGeoIntel(lat, lon) {
  const cacheKey = `geointel_${lat.toFixed(3)}_${lon.toFixed(3)}`
  
  if (cache.has(cacheKey)) {
    const cached = cache.get(cacheKey)
    if (Date.now() - cached.timestamp < CACHE_TTL) {
      return cached.data
    }
  }
  
  try {
    console.log('[GeoIntel] Fetching comprehensive geo-intel:', lat, lon)
    const url = `${API_BASE}/api/geo-intel?lat=${lat}&lon=${lon}`
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`Geo-intel API failed: ${response.status}`)
    }
    
    const data = await response.json()
    cache.set(cacheKey, { data, timestamp: Date.now() })
    
    return data
  } catch (error) {
    console.error('[GeoIntel] Geo-intel fetch error:', error)
    return getSimulatedGeoIntel(lat, lon)
  }
}

/**
 * Fetch infrastructure data
 */
export async function fetchInfrastructureLayer(lat, lon) {
  try {
    const url = lat && lon 
      ? `${API_BASE}/api/infrastructure?lat=${lat}&lon=${lon}`
      : `${API_BASE}/api/infrastructure`
    
    const response = await fetch(url)
    
    if (!response.ok) {
      throw new Error(`Infrastructure API failed: ${response.status}`)
    }
    
    const data = await response.json()
    return data.facilities || []
  } catch (error) {
    console.error('[GeoIntel] Infrastructure fetch error:', error)
    return getSimulatedInfrastructure(lat, lon)
  }
}

/**
 * AI Risk Score Calculation
 */
export function calculateRiskScore(weather, nasa) {
  let score = 0
  
  if (!weather) return 0
  
  // Wind Score (up to 40 points)
  const windSpeed = weather.wind_speed || 0
  if (windSpeed > 14) {
    score += 40
  } else if (windSpeed > 8) {
    score += 20
  } else if (windSpeed > 4) {
    score += 10
  }
  
  // Rainfall Score (up to 30 points)
  const rain = weather.rain?.['1h'] || 0
  if (rain > 10) {
    score += 30
  } else if (rain > 2) {
    score += 15
  }
  
  // Temperature Score (up to 15 points)
  const temp = weather.temperature || weather.main?.temp || 20
  if (temp > 40 || temp < -5) {
    score += 15
  }
  
  // Condition Score (up to 15 points)
  const condition = (weather.description || '').toLowerCase()
  const severeConditions = ['thunderstorm', 'tornado', 'extreme', 'hurricane', 'cyclone']
  if (severeConditions.some(c => condition.includes(c))) {
    score += 15
  }
  
  // NASA precipitation contribution
  if (nasa?.precipitation > 10) {
    score += 20
  } else if (nasa?.precipitation > 5) {
    score += 10
  }
  
  return Math.min(score, 100)
}

/**
 * Simulated weather data (fallback)
 */
function getSimulatedWeather(lat, lon) {
  return {
    name: 'Simulated Location',
    main: {
      temp: 25 + (lat * 10) % 10,
      humidity: 50 + (lon * 5) % 40,
      pressure: 1013 + ((lat + lon) * 10) % 20
    },
    wind: {
      speed: 3 + (lat + lon) % 8,
      deg: ((lon * 10) % 360)
    },
    weather: [{ description: 'Partly cloudy', main: 'Clouds' }],
    clouds: { all: ((lat + lon) * 10) % 100 },
    visibility: 10000
  }
}

/**
 * Simulated NASA data (fallback)
 */
function getSimulatedNasaData(lat, lon) {
  return {
    temperature: 25 + (lat * 5) % 15,
    precipitation: (lon * 2) % 10,
    solar_radiation: 500 + (lat + lon) % 300,
    relative_humidity: 50 + (lon * 3) % 40
  }
}

/**
 * Simulated geo-intel (fallback)
 */
function getSimulatedGeoIntel(lat, lon) {
  const weather = getSimulatedWeather(lat, lon)
  const nasa = getSimulatedNasaData(lat, lon)
  const riskScore = calculateRiskScore(weather, nasa)
  
  return {
    coordinates: { lat, lon },
    weather,
    nasa_data: nasa,
    infrastructure: getSimulatedInfrastructure(lat, lon),
    risk_score: riskScore,
    risk_level: riskScore >= 80 ? 'critical' : riskScore >= 60 ? 'high' : riskScore >= 40 ? 'elevated' : 'low',
    timestamp: new Date().toISOString()
  }
}

/**
 * Simulated infrastructure (fallback)
 */
function getSimulatedInfrastructure(lat, lon) {
  return [
    { id: 'h_1', name: 'Strategic Shelter Alpha', lat: lat + 0.005, lon: lon + 0.005, type: 'shelter', distance_km: 0.5 },
    { id: 'h_2', name: 'Communication Relay 09', lat: lat - 0.008, lon: lon + 0.002, type: 'comm', distance_km: 0.9 },
    { id: 'h_3', name: 'Emergency Fuel Reserve', lat: lat + 0.004, lon: lon - 0.006, type: 'resource', distance_km: 0.7 }
  ]
}

/**
 * Clear cache
 */
export function clearCache() {
  cache.clear()
  console.log('[GeoIntel] Cache cleared')
}

