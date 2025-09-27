"""
Pydantic schemas for location operations
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LocationBase(BaseModel):
    """Base location schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    building: Optional[str] = Field(None, max_length=100)
    floor: Optional[str] = Field(None, max_length=50)
    room: Optional[str] = Field(None, max_length=100)
    zone: Optional[str] = Field(None, max_length=100)
    responsible_person: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)


class LocationCreate(LocationBase):
    """Schema for creating a new location"""
    pass


class LocationUpdate(BaseModel):
    """Schema for updating a location"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    building: Optional[str] = Field(None, max_length=100)
    floor: Optional[str] = Field(None, max_length=50)
    room: Optional[str] = Field(None, max_length=100)
    zone: Optional[str] = Field(None, max_length=100)
    responsible_person: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)


class LocationResponse(LocationBase):
    """Schema for location response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class LocationListResponse(BaseModel):
    """Schema for location list response"""
    locations: List[LocationResponse]
    total: int
    page: int
    size: int
