"""
Location endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.location import Location
from backend.models.user import User
from backend.auth.dependencies import get_current_active_user, get_current_admin_user
from backend.schemas.location import LocationCreate, LocationUpdate, LocationResponse, LocationListResponse

router = APIRouter()


@router.get("/", response_model=LocationListResponse)
async def get_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of locations"""
    query = db.query(Location)
    total = query.count()
    locations = query.offset(skip).limit(limit).all()
    
    return LocationListResponse(
        locations=[LocationResponse.from_orm(location) for location in locations],
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get location by ID"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    return location


@router.post("/", response_model=LocationResponse)
async def create_location(
    location_data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new location"""
    db_location = Location(**location_data.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    
    return db_location


@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update location"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    update_data = location_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    
    db.commit()
    db.refresh(location)
    
    return location


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete location"""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location not found"
        )
    
    db.delete(location)
    db.commit()
    
    return {"message": "Location deleted successfully"}
