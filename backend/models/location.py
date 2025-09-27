"""
Location model for IFC monitoring system
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class Location(Base):
    """Location model for organizing sensors"""
    
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    
    # Geographic information
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)  # meters above sea level
    
    # Location hierarchy
    building = Column(String(100))
    floor = Column(String(50))
    room = Column(String(100))
    zone = Column(String(100))  # e.g., "Production Area", "Storage"
    
    # Contact information
    responsible_person = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sensors = relationship("Sensor", back_populates="location")
    
    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}')>"
