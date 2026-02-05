import { useState, useEffect } from 'react';
import { fetchCurrentWeather, fetchNasaPower, calculateRiskScore } from '../services/geoIntelligenceService';

const RiskPopup = ({ lat, lon }) => {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getIntelligence = async () => {
            setLoading(true);
            try {
                const [weather, nasa] = await Promise.all([
                    fetchCurrentWeather(lat, lon),
                    fetchNasaPower(lat, lon)
                ]);

                if (!weather) throw new Error("Could not retrieve geo-intelligence");

                const score = calculateRiskScore(weather, nasa);

                setData({
                    weather,
                    nasa,
                    score
                });
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        getIntelligence();
    }, [lat, lon]);

    if (loading) {
        return (
            <div className="risk-popup-loading">
                <div className="spinner"></div>
                <span>Analyzing Geo-Intelligence...</span>
            </div>
        );
    }

    if (error || !data) {
        return <div className="risk-popup-error">⚠️ Service Unavailable</div>;
    }

    const { weather, nasa, score } = data;

    // Auto-calculated Risk Indicator (User Requirement)
    const isHighRisk = (weather.wind.speed * 3.6) > 50 || (weather.rain?.['1h'] > 0) || (nasa?.precipitation > 0);

    const getBadgeColor = (s, high) => {
        if (high || s >= 70) return 'red';
        if (s >= 40) return 'orange';
        return 'green';
    };

    return (
        <div className="intel-card">
            <div className="intel-header" style={{ marginBottom: '10px' }}>
                <div style={{ fontSize: '14px', fontWeight: 'bold' }}>{weather.name || "Regional Scan"}</div>
            </div>

            <div className={`intel-badge ${getBadgeColor(score, isHighRisk)}`}>
                AI RISK: {isHighRisk ? 'HIGH (CRITICAL)' : (score > 40 ? 'ELEVATED' : 'STABLE')}
            </div>

            <div className="intel-section">
                <div className="section-label">Atmospheric Intelligence</div>
                <div className="intel-grid">
                    <div className="intel-item">
                        <span className="label">Temp</span>
                        <span className="value">{weather.main.temp}°C</span>
                    </div>
                    <div className="intel-item">
                        <span className="label">Wind</span>
                        <span className="value">{(weather.wind.speed * 3.6).toFixed(1)} km/h</span>
                    </div>
                    <div className="intel-item">
                        <span className="label">Humidity</span>
                        <span className="value">{weather.main.humidity}%</span>
                    </div>
                    <div className="intel-item">
                        <span className="label">Weather</span>
                        <span className="value">{weather.weather[0].description}</span>
                    </div>
                </div>
            </div>

            <div className="intel-divider"></div>

            <div className="intel-section">
                <div className="section-label">NASA Environmental Monitoring</div>
                <div className="intel-grid">
                    <div className="intel-item">
                        <span className="label">SFC Temp</span>
                        <span className="value">{nasa?.temp?.toFixed(1)}°C</span>
                    </div>
                    <div className="intel-item">
                        <span className="label">Precip</span>
                        <span className="value">{nasa?.precipitation?.toFixed(2)} mm</span>
                    </div>
                </div>
                {nasa?.precipitation > 0.5 && (
                    <div className="intel-anomaly">
                        ⚠️ High Precipitation Anomaly Detected
                    </div>
                )}
            </div>

            <div className="intel-coordinates">
                COORD: {lat.toFixed(4)}, {lon.toFixed(4)}
            </div>
        </div>
    );
};

export default RiskPopup;
