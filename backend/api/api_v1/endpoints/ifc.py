"""
IFC file endpoints
"""

import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.ifc_file import IFCFile
from backend.models.ifc_space import IFCSpace
from backend.models.user import User
from backend.auth.dependencies import get_current_active_user, get_current_admin_user
from backend.schemas.ifc import IFCFileResponse, IFCFileUpdate, IFCFileListResponse, IFCSpaceResponse, IFCSpaceListResponse
from backend.services.ifc_processor import IFCProcessor

router = APIRouter()

# Configuration
UPLOAD_DIR = "uploads/ifc"
ALLOWED_EXTENSIONS = [".ifc"]
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/files", response_model=IFCFileListResponse)
async def get_ifc_files(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of uploaded IFC files"""
    query = db.query(IFCFile)
    total = query.count()
    ifc_files = query.offset(skip).limit(limit).order_by(IFCFile.created_at.desc()).all()
    
    return IFCFileListResponse(
        ifc_files=[IFCFileResponse.from_orm(file) for file in ifc_files],
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/files/{file_id}", response_model=IFCFileResponse)
async def get_ifc_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get IFC file by ID"""
    ifc_file = db.query(IFCFile).filter(IFCFile.id == file_id).first()
    if not ifc_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IFC file not found"
        )
    return ifc_file


@router.post("/upload", response_model=IFCFileResponse)
async def upload_ifc_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Upload IFC file"""
    
    # Validate file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Validate file size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Maximum size is 100MB"
        )
    
    # Generate unique filename
    import uuid
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(file_content)
    
    # Create database record
    ifc_file = IFCFile(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=len(file_content),
        uploaded_by=current_user.id
    )
    
    db.add(ifc_file)
    db.commit()
    db.refresh(ifc_file)
    
    # Start processing in background
    try:
        processor = IFCProcessor()
        await processor.process_ifc_file(ifc_file.id, db)
    except Exception as e:
        # Update processing status
        ifc_file.processing_status = "failed"
        ifc_file.processing_error = str(e)
        db.commit()
    
    return ifc_file


@router.put("/files/{file_id}", response_model=IFCFileResponse)
async def update_ifc_file(
    file_id: int,
    file_data: IFCFileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update IFC file metadata"""
    ifc_file = db.query(IFCFile).filter(IFCFile.id == file_id).first()
    if not ifc_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IFC file not found"
        )
    
    update_data = file_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ifc_file, field, value)
    
    db.commit()
    db.refresh(ifc_file)
    
    return ifc_file


@router.delete("/files/{file_id}")
async def delete_ifc_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete IFC file and its data"""
    ifc_file = db.query(IFCFile).filter(IFCFile.id == file_id).first()
    if not ifc_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IFC file not found"
        )
    
    # Delete physical file
    if os.path.exists(ifc_file.file_path):
        os.remove(ifc_file.file_path)
    
    # Delete database records
    db.delete(ifc_file)
    db.commit()
    
    return {"message": "IFC file deleted successfully"}


@router.get("/files/{file_id}/spaces", response_model=IFCSpaceListResponse)
async def get_ifc_spaces(
    file_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    space_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get spaces from IFC file"""
    query = db.query(IFCSpace).filter(IFCSpace.ifc_file_id == file_id)
    
    if space_type:
        query = query.filter(IFCSpace.space_type == space_type)
    
    total = query.count()
    spaces = query.offset(skip).limit(limit).all()
    
    return IFCSpaceListResponse(
        spaces=[IFCSpaceResponse.from_orm(space) for space in spaces],
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.post("/files/{file_id}/process")
async def reprocess_ifc_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Reprocess IFC file"""
    ifc_file = db.query(IFCFile).filter(IFCFile.id == file_id).first()
    if not ifc_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IFC file not found"
        )
    
    # Reset processing status
    ifc_file.processing_status = "pending"
    ifc_file.processing_error = None
    db.commit()
    
    # Start processing
    try:
        processor = IFCProcessor()
        await processor.process_ifc_file(ifc_file.id, db)
        return {"message": "IFC file processing started"}
    except Exception as e:
        ifc_file.processing_status = "failed"
        ifc_file.processing_error = str(e)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing failed: {str(e)}"
        )
