"""
Alert model for IFC monitoring system
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from backend.core.database import Base


class AlertSeverity(str, enum.Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, enum.Enum):
    """Alert status"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


class Alert(Base):
    """Alert model for system notifications"""
    
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    alert_type = Column(String(50), nullable=False)  # threshold_exceeded, sensor_offline, etc.
    severity = Column(Enum(AlertSeverity), nullable=False, default=AlertSeverity.MEDIUM)
    status = Column(Enum(AlertStatus), nullable=False, default=AlertStatus.ACTIVE)
    
    # Alert details
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    threshold_value = Column(Float)
    actual_value = Column(Float)
    
    # Timestamps
    triggered_at = Column(DateTime(timezone=True), nullable=False, index=True)
    acknowledged_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    acknowledged_by = Column(Integer, ForeignKey("users.id"))
    
    # Notification settings
    email_sent = Column(Boolean, default=False)
    sms_sent = Column(Boolean, default=False)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sensor = relationship("Sensor", back_populates="alerts")
    acknowledged_user = relationship("User", foreign_keys=[acknowledged_by])
    
    def __repr__(self):
        return f"<Alert(id={self.id}, type='{self.alert_type}', severity='{self.severity}', status='{self.status}')>"
