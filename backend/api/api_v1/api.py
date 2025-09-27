"""
Main API router for version 1
"""

from fastapi import APIRouter
from backend.api.api_v1.endpoints import auth, sensors, readings, alerts, locations, users, ifc

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
api_router.include_router(readings.router, prefix="/readings", tags=["readings"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(ifc.router, prefix="/ifc", tags=["ifc"])
