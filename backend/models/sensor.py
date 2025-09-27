"""
Sensor model for IFC monitoring system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class Sensor(Base):
    """Sensor model for monitoring various parameters"""
    
    __tablename__ = "sensors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    sensor_type = Column(String(50), nullable=False)  # temperature, humidity, pressure, etc.
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    device_id = Column(String(100), unique=True, nullable=False, index=True)
    model = Column(String(100))
    manufacturer = Column(String(100))
    serial_number = Column(String(100), unique=True)
    
    # Calibration data
    min_value = Column(Float)
    max_value = Column(Float)
    unit = Column(String(20))  # °C, %, hPa, etc.
    
    # Configuration
    is_active = Column(Boolean, default=True)
    update_interval = Column(Integer, default=60)  # seconds
    alert_threshold_min = Column(Float)
    alert_threshold_max = Column(Float)
    
    # Metadata
    description = Column(Text)
    installation_date = Column(DateTime(timezone=True))
    last_calibration = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    location = relationship("Location", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="sensor", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Sensor(id={self.id}, name='{self.name}', type='{self.sensor_type}')>"
