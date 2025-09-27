"""
Sensor readings endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.core.database import get_db
from backend.models.reading import SensorReading
from backend.models.user import User
from backend.auth.dependencies import get_current_active_user
from backend.schemas.reading import ReadingResponse, ReadingCreate, ReadingListResponse
from sqlalchemy.sql import func

router = APIRouter()


@router.get("/", response_model=ReadingListResponse)
async def get_readings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sensor_id: Optional[int] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get sensor readings with optional filtering"""
    query = db.query(SensorReading)
    
    # Apply filters
    if sensor_id:
        query = query.filter(SensorReading.sensor_id == sensor_id)
    if start_time:
        query = query.filter(SensorReading.timestamp >= start_time)
    if end_time:
        query = query.filter(SensorReading.timestamp <= end_time)
    
    # Order by timestamp descending
    query = query.order_by(SensorReading.timestamp.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    readings = query.offset(skip).limit(limit).all()
    
    return ReadingListResponse(
        readings=[ReadingResponse.from_orm(reading) for reading in readings],
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.post("/", response_model=ReadingResponse)
async def create_reading(
    reading_data: ReadingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create new sensor reading"""
    db_reading = SensorReading(**reading_data.dict())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    
    return db_reading


@router.get("/latest")
async def get_latest_readings(
    sensor_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get latest readings for specified sensors or all sensors"""
    from sqlalchemy import func
    
    query = db.query(
        SensorReading.sensor_id,
        SensorReading.value,
        SensorReading.timestamp,
        func.max(SensorReading.timestamp).label('max_timestamp')
    ).group_by(SensorReading.sensor_id)
    
    if sensor_ids:
        query = query.filter(SensorReading.sensor_id.in_(sensor_ids))
    
    # Get latest reading for each sensor
    latest_readings = db.query(SensorReading).join(
        query.subquery(),
        (SensorReading.sensor_id == query.subquery().c.sensor_id) &
        (SensorReading.timestamp == query.subquery().c.max_timestamp)
    ).all()
    
    return [ReadingResponse.from_orm(reading) for reading in latest_readings]
