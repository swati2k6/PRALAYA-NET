"""
PRALAYA-NET Backend - FastAPI Application
Main entry point for the disaster management system
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from api.trigger_api import router as trigger_router
from api.drone_api import router as drone_router
from api.satellite_api import router as satellite_router
from api.alerts_api import router as alerts_router
from api.risk_alert_api import router as risk_alert_router
from config import APP_NAME, VERSION, CORS_ORIGINS

# Import middleware (but we'll add them selectively)
# from middleware import (
#     RateLimitMiddleware,
#     InputValidationMiddleware,
#     SecurityHeadersMiddleware,
#     RequestLoggingMiddleware
# )

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="Unified Disaster Command System - AI-powered disaster prediction and response"
)

# Security & Performance Middleware Stack (order matters)
# Temporarily disabled - will re-enable after basic testing
# app.add_middleware(RequestLoggingMiddleware)
# app.add_middleware(SecurityHeadersMiddleware)
# app.add_middleware(InputValidationMiddleware)
# app.add_middleware(RateLimitMiddleware, requests_per_minute=100)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trigger_router, prefix="/api/trigger", tags=["Trigger"])
app.include_router(drone_router, prefix="/api/drones", tags=["Drones"])
app.include_router(satellite_router, prefix="/api/satellite", tags=["Satellite"])
app.include_router(alerts_router, prefix="/api/orchestration/alerts", tags=["Alerts"])
app.include_router(risk_alert_router, tags=["Risk Alert"])

@app.get("/")
def home():
    """Root endpoint - health check"""
    return {
        "status": "online",
        "system": APP_NAME,
        "version": VERSION,
        "message": "PRALAYA-NET backend is operational"
    }

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "api": "operational",
            "ai_models": "loaded",
            "orchestration": "ready"
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": type(exc).__name__}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
