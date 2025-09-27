"""
IFC Space model for storing spaces extracted from IFC files
"""

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class IFCSpace(Base):
    """IFC Space model for storing building spaces"""
    
    __tablename__ = "ifc_spaces"
    
    id = Column(Integer, primary_key=True, index=True)
    ifc_file_id = Column(Integer, ForeignKey("ifc_files.id"), nullable=False)
    
    # IFC Space properties
    ifc_id = Column(String(100), nullable=False, index=True)  # IFC GlobalId
    name = Column(String(255))
    long_name = Column(String(500))
    description = Column(Text)
    
    # Space type
    space_type = Column(String(100))  # room, corridor, stair, elevator, etc.
    usage_type = Column(String(100))  # office, storage, mechanical, etc.
    
    # Dimensions
    area = Column(Float)  # square meters
    volume = Column(Float)  # cubic meters
    height = Column(Float)  # meters
    
    # Coordinates (if available)
    x_coordinate = Column(Float)
    y_coordinate = Column(Float)
    z_coordinate = Column(Float)
    
    # Level information
    level_name = Column(String(100))
    level_elevation = Column(Float)
    
    # Relationships
    ifc_file = relationship("IFCFile")
    
    def __repr__(self):
        return f"<IFCSpace(id={self.id}, name='{self.name}', type='{self.space_type}')>"
