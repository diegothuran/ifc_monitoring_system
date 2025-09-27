"""
Pydantic schemas for sensor reading operations
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ReadingBase(BaseModel):
    """Base reading schema"""
    sensor_id: int
    value: float
    timestamp: datetime
    quality_score: float = Field(1.0, ge=0.0, le=1.0)
    is_valid: int = Field(1, ge=0, le=1)


class ReadingCreate(ReadingBase):
    """Schema for creating a new reading"""
    pass


class ReadingResponse(ReadingBase):
    """Schema for reading response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReadingListResponse(BaseModel):
    """Schema for reading list response"""
    readings: List[ReadingResponse]
    total: int
    page: int
    size: int
