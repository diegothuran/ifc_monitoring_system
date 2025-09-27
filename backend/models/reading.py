"""
Sensor reading model for IFC monitoring system
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base


class SensorReading(Base):
    """Sensor reading model for storing measurement data"""
    
    __tablename__ = "sensor_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Quality indicators
    quality_score = Column(Float, default=1.0)  # 0.0 to 1.0
    is_valid = Column(Integer, default=1)  # 1 = valid, 0 = invalid
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    sensor = relationship("Sensor", back_populates="readings")
    
    # Indexes for performance
    __table_args__ = (
        Index('ix_sensor_timestamp', 'sensor_id', 'timestamp'),
        Index('ix_timestamp_value', 'timestamp', 'value'),
    )
    
    def __repr__(self):
        return f"<SensorReading(id={self.id}, sensor_id={self.sensor_id}, value={self.value}, timestamp='{self.timestamp}')>"
