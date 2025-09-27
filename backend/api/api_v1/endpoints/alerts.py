"""
Alert endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.alert import Alert, AlertStatus
from backend.models.user import User
from backend.auth.dependencies import get_current_active_user
from backend.schemas.alert import AlertResponse, AlertUpdate, AlertListResponse
from sqlalchemy.sql import func

router = APIRouter()


@router.get("/", response_model=AlertListResponse)
async def get_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[AlertStatus] = None,
    severity: Optional[str] = None,
    sensor_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get alerts with optional filtering"""
    query = db.query(Alert)
    
    # Apply filters
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    if sensor_id:
        query = query.filter(Alert.sensor_id == sensor_id)
    
    # Order by triggered_at descending
    query = query.order_by(Alert.triggered_at.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    alerts = query.offset(skip).limit(limit).all()
    
    return AlertListResponse(
        alerts=[AlertResponse.from_orm(alert) for alert in alerts],
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get alert by ID"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    return alert


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: int,
    alert_data: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update alert status"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    # Update fields
    update_data = alert_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(alert, field, value)
    
    # Set timestamps based on status
    if alert_data.status == AlertStatus.ACKNOWLEDGED and not alert.acknowledged_at:
        alert.acknowledged_at = func.now()
        alert.acknowledged_by = current_user.id
    elif alert_data.status == AlertStatus.RESOLVED and not alert.resolved_at:
        alert.resolved_at = func.now()
    
    db.commit()
    db.refresh(alert)
    
    return alert
