"""
Sensor endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.sensor import Sensor
from backend.models.user import User
from backend.auth.dependencies import get_current_active_user, get_current_admin_user
from backend.schemas.sensor import SensorCreate, SensorUpdate, SensorResponse, SensorListResponse

router = APIRouter()


@router.get("/", response_model=SensorListResponse)
async def get_sensors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sensor_type: Optional[str] = None,
    location_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of sensors with optional filtering"""
    query = db.query(Sensor)
    
    # Apply filters
    if sensor_type:
        query = query.filter(Sensor.sensor_type == sensor_type)
    if location_id:
        query = query.filter(Sensor.location_id == location_id)
    if is_active is not None:
        query = query.filter(Sensor.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    sensors = query.offset(skip).limit(limit).all()
    
    return SensorListResponse(
        sensors=[SensorResponse.from_orm(sensor) for sensor in sensors],
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/{sensor_id}", response_model=SensorResponse)
async def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get sensor by ID"""
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found"
        )
    return sensor


@router.post("/", response_model=SensorResponse)
async def create_sensor(
    sensor_data: SensorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new sensor"""
    # Check if device_id already exists
    if db.query(Sensor).filter(Sensor.device_id == sensor_data.device_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device ID already exists"
        )
    
    # Check if serial_number already exists
    if sensor_data.serial_number:
        if db.query(Sensor).filter(Sensor.serial_number == sensor_data.serial_number).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Serial number already exists"
            )
    
    db_sensor = Sensor(**sensor_data.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    
    return db_sensor


@router.put("/{sensor_id}", response_model=SensorResponse)
async def update_sensor(
    sensor_id: int,
    sensor_data: SensorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update sensor"""
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found"
        )
    
    # Update fields
    update_data = sensor_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sensor, field, value)
    
    db.commit()
    db.refresh(sensor)
    
    return sensor


@router.delete("/{sensor_id}")
async def delete_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete sensor"""
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found"
        )
    
    db.delete(sensor)
    db.commit()
    
    return {"message": "Sensor deleted successfully"}
