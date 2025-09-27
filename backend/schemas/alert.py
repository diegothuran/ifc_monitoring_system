"""
Pydantic schemas for alert operations
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from backend.models.alert import AlertSeverity, AlertStatus


class AlertBase(BaseModel):
    """Base alert schema"""
    sensor_id: int
    alert_type: str
    severity: AlertSeverity
    title: str
    message: str
    threshold_value: Optional[float] = None
    actual_value: Optional[float] = None


class AlertCreate(AlertBase):
    """Schema for creating a new alert"""
    triggered_at: datetime


class AlertUpdate(BaseModel):
    """Schema for updating an alert"""
    status: Optional[AlertStatus] = None
    message: Optional[str] = None


class AlertResponse(AlertBase):
    """Schema for alert response"""
    id: int
    status: AlertStatus
    triggered_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    acknowledged_by: Optional[int] = None
    email_sent: bool
    sms_sent: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    """Schema for alert list response"""
    alerts: List[AlertResponse]
    total: int
    page: int
    size: int
