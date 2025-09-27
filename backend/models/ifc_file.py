"""
IFC File model for storing uploaded IFC files
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class IFCFile(Base):
    """IFC File model for storing building information"""
    
    __tablename__ = "ifc_files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), default="IFC")
    
    # IFC specific metadata
    ifc_version = Column(String(20))
    project_name = Column(String(255))
    project_description = Column(Text)
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    processing_status = Column(String(50), default="pending")  # pending, processing, completed, failed
    processing_error = Column(Text)
    
    # Building dimensions (if extracted)
    building_width = Column(Float)
    building_height = Column(Float)
    building_depth = Column(Float)
    
    # Metadata
    uploaded_by = Column(Integer)  # User ID who uploaded
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<IFCFile(id={self.id}, filename='{self.filename}', status='{self.processing_status}')>"
