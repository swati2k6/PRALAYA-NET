/**
 * geoIntelligenceService.js
 * Advanced Geo-Intelligence for National Disaster Command
 */

const CACHE_TTL = 5 * 60 * 1000; // 5 minute cache
const cache = new Map();

const OW_KEY = import.meta.env.VITE_OPENWEATHER_API_KEY;
const DATA_GOV_KEY = import.meta.env.VITE_DATA_GOV_KEY;

/**
 * Fetch Current Weather from OpenWeather
 */
export async function fetchCurrentWeather(lat, lon) {
    const cacheKey = `weather_${lat.toFixed(3)}_${lon.toFixed(3)}`;
    if (cache.has(cacheKey) && (Date.now() - cache.get(cacheKey).timestamp < CACHE_TTL)) {
        return cache.get(cacheKey).data;
    }

    try {
        const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${OW_KEY}&units=metric`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("Weather API failed");
        const data = await response.json();

        cache.set(cacheKey, { data, timestamp: Date.now() });
        return data;
    } catch (error) {
        console.error("Geo-Intel Error (Weather):", error);
        return null;
    }
}

/**
 * Fetch Climate Data from NASA POWER
 */
export async function fetchNasaPower(lat, lon) {
    const cacheKey = `nasa_${lat.toFixed(3)}_${lon.toFixed(3)}`;
    if (cache.has(cacheKey) && (Date.now() - cache.get(cacheKey).timestamp < CACHE_TTL)) {
        return cache.get(cacheKey).data;
    }

    try {
        // NASA POWER API - Hourly data for temperature and precipitation
        const url = `https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=T2M,PRECTOTCORR&community=RE&longitude=${lon}&latitude=${lat}&format=JSON`;
        const response = await fetch(url);
        if (!response.ok) throw new Error("NASA POWER failed");
        const data = await response.json();

        // Extract latest values
        const properties = data.properties.parameter;
        const latestTime = Object.keys(properties.T2M).sort().reverse()[0];

        const result = {
            temp: properties.T2M[latestTime],
            precipitation: properties.PRECTOTCORR[latestTime],
            raw: data
        };

        cache.set(cacheKey, { data: result, timestamp: Date.now() });
        return result;
    } catch (error) {
        console.error("Geo-Intel Error (NASA):", error);
        return null;
    }
}

/**
 * Fetch Infrastructure Intelligence from Data.gov
 * (Simulated logic using Data.gov context if key is missing, 
 * real implementation targets specific GeoJSON endpoints if available)
 */
export async function fetchInfrastructureLayer(lat, lon) {
    if (!DATA_GOV_KEY || DATA_GOV_KEY.includes("your")) {
        // Return high-fidelity simulation markers based on geolocation
        // In a real environment, this would call specific hazard dataset APIs
        return [
            { id: 'h_1', name: 'Strategic Shelter Alpha', lat: lat + 0.005, lon: lon + 0.005, type: 'shelter' },
            { id: 'h_2', name: 'Communication Relay 09', lat: lat - 0.008, lon: lon + 0.002, type: 'comm' },
            { id: 'h_3', name: 'Emergency Fuel Reserve', lat: lat + 0.004, lon: lon - 0.006, type: 'resource' }
        ];
    }

    // Example: Fetch Hospital locations from Data.gov (HHS Dataset)
    // Note: Most Data.gov spatial datasets are massive, so we often use their search API
    // or specifically cached GeoJSONs.
    return [];
}

/**
 * AI Risk Score Calculation Logic
 */
export function calculateRiskScore(weather, nasa) {
    let score = 0;

    if (!weather) return 0;

    // Wind Score (Up to 40 points)
    const windSpeed = weather.wind?.speed || 0;
    if (windSpeed > 14) score += 40; // 50 km/h approx
    else if (windSpeed > 8) score += 20;
    else if (windSpeed > 4) score += 10;

    // Rainfall Score (Up to 30 points)
    const rain = weather.rain?.['1h'] || 0;
    const precipitation = nasa?.precipitation || 0;
    if (rain > 10 || precipitation > 10) score += 30;
    else if (rain > 2 || precipitation > 2) score += 15;

    // Temperature Score (Up to 15 points)
    const temp = weather.main?.temp || 0;
    if (temp > 40 || temp < -5) score += 15;

    // Condition Score (Up to 15 points)
    const condition = weather.weather?.[0]?.main?.toLowerCase();
    if (['thunderstorm', 'tornado', 'extreme', 'hurricane'].includes(condition)) score += 15;

    return Math.min(score, 100);
}
