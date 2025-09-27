"""
Pydantic schemas for sensor-related operations
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from backend.models.sensor import Sensor


class SensorBase(BaseModel):
    """Base sensor schema"""
    name: str = Field(..., min_length=1, max_length=100)
    sensor_type: str = Field(..., min_length=1, max_length=50)
    location_id: int
    device_id: str = Field(..., min_length=1, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    unit: Optional[str] = Field(None, max_length=20)
    update_interval: int = Field(60, ge=1)
    alert_threshold_min: Optional[float] = None
    alert_threshold_max: Optional[float] = None
    description: Optional[str] = None
    installation_date: Optional[datetime] = None
    last_calibration: Optional[datetime] = None


class SensorCreate(SensorBase):
    """Schema for creating a new sensor"""
    pass


class SensorUpdate(BaseModel):
    """Schema for updating a sensor"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    sensor_type: Optional[str] = Field(None, min_length=1, max_length=50)
    location_id: Optional[int] = None
    device_id: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=100)
    serial_number: Optional[str] = Field(None, max_length=100)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    unit: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    update_interval: Optional[int] = Field(None, ge=1)
    alert_threshold_min: Optional[float] = None
    alert_threshold_max: Optional[float] = None
    description: Optional[str] = None
    installation_date: Optional[datetime] = None
    last_calibration: Optional[datetime] = None


class SensorResponse(SensorBase):
    """Schema for sensor response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SensorListResponse(BaseModel):
    """Schema for sensor list response"""
    sensors: List[SensorResponse]
    total: int
    page: int
    size: int
