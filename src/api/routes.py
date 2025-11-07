from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional
import json

app = FastAPI(title="EcoVerse API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/environmental-data")
async def get_environmental_data(range: str = "24h"):
    """Get environmental data for specified time range"""
    # TODO: Connect to your database/agents
    # This is a placeholder - replace with actual data fetching
    return {
        "data": [
            {"time": "00:00", "temp": 22, "humidity": 65, "aqi": 45, "co2": 410},
            # ... more data points
        ],
        "range": range,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/agents/status")
async def get_agent_status():
    """Get status of all agents"""
    # TODO: Query your agent orchestrator
    return {
        "agents": [
            {"name": "Sensing", "status": "active", "tasks": 156, "accuracy": 98.5},
            {"name": "Analysis", "status": "active", "tasks": 89, "accuracy": 95.2},
            {"name": "Alert", "status": "active", "tasks": 12, "accuracy": 100},
            {"name": "Coordination", "status": "active", "tasks": 234, "accuracy": 97.8},
        ]
    }

@app.get("/api/v1/alerts")
async def get_alerts(limit: int = 10):
    """Get recent alerts"""
    # TODO: Query your alert agent/database
    return {
        "alerts": [
            {
                "id": 1,
                "type": "warning",
                "message": "High PM2.5 detected in Zone A",
                "location": "Mumbai",
                "time": "2 min ago",
                "severity": "high"
            }
        ],
        "total": 1
    }

@app.get("/api/v1/pollution/distribution")
async def get_pollution_distribution():
    """Get pollution type distribution"""
    return {
        "distribution": [
            {"name": "CO2", "value": 42, "color": "#10b981"},
            {"name": "PM2.5", "value": 28, "color": "#f59e0b"},
            {"name": "NO2", "value": 18, "color": "#ef4444"},
            {"name": "SO2", "value": 12, "color": "#8b5cf6"},
        ]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    try:
        while True:
            # TODO: Stream real-time data from your agents
            data = {
                "type": "environmental_update",
                "data": {
                    "temp": 25,
                    "humidity": 60,
                    "aqi": 50,
                    "timestamp": datetime.now().isoformat()
                }
            }
            await websocket.send_json(data)
            await asyncio.sleep(5)  # Send updates every 5 seconds
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()
