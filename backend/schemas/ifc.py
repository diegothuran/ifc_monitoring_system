"""
Pydantic schemas for IFC file operations
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IFCFileBase(BaseModel):
    """Base IFC file schema"""
    filename: str
    original_filename: str
    file_size: int
    ifc_version: Optional[str] = None
    project_name: Optional[str] = None
    project_description: Optional[str] = None


class IFCFileCreate(BaseModel):
    """Schema for creating IFC file record"""
    filename: str
    original_filename: str
    file_size: int
    ifc_version: Optional[str] = None
    project_name: Optional[str] = None
    project_description: Optional[str] = None


class IFCFileUpdate(BaseModel):
    """Schema for updating IFC file"""
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    is_processed: Optional[bool] = None
    processing_status: Optional[str] = None
    processing_error: Optional[str] = None
    building_width: Optional[float] = None
    building_height: Optional[float] = None
    building_depth: Optional[float] = None


class IFCFileResponse(IFCFileBase):
    """Schema for IFC file response"""
    id: int
    file_path: str
    file_type: str
    is_processed: bool
    processing_status: str
    processing_error: Optional[str] = None
    building_width: Optional[float] = None
    building_height: Optional[float] = None
    building_depth: Optional[float] = None
    uploaded_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class IFCSpaceBase(BaseModel):
    """Base IFC space schema"""
    ifc_id: str
    name: Optional[str] = None
    long_name: Optional[str] = None
    description: Optional[str] = None
    space_type: Optional[str] = None
    usage_type: Optional[str] = None
    area: Optional[float] = None
    volume: Optional[float] = None
    height: Optional[float] = None
    x_coordinate: Optional[float] = None
    y_coordinate: Optional[float] = None
    z_coordinate: Optional[float] = None
    level_name: Optional[str] = None
    level_elevation: Optional[float] = None


class IFCSpaceResponse(IFCSpaceBase):
    """Schema for IFC space response"""
    id: int
    ifc_file_id: int
    
    class Config:
        from_attributes = True


class IFCFileListResponse(BaseModel):
    """Schema for IFC file list response"""
    ifc_files: List[IFCFileResponse]
    total: int
    page: int
    size: int


class IFCSpaceListResponse(BaseModel):
    """Schema for IFC space list response"""
    spaces: List[IFCSpaceResponse]
    total: int
    page: int
    size: int
