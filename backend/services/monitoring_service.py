"""
Monitoring service for IFC system
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.models.sensor import Sensor
from backend.models.reading import SensorReading
from backend.models.alert import Alert, AlertSeverity, AlertStatus
from backend.core.config import settings

logger = logging.getLogger(__name__)


class MonitoringService:
    """Service for monitoring sensors and processing alerts"""
    
    def __init__(self):
        self.is_running = False
        self.task = None
    
    async def start_monitoring(self):
        """Start the monitoring service"""
        if self.is_running:
            logger.warning("Monitoring service is already running")
            return
        
        self.is_running = True
        logger.info("Starting monitoring service...")
        
        # Start background task
        self.task = asyncio.create_task(self._monitoring_loop())
    
    async def stop_monitoring(self):
        """Stop the monitoring service"""
        if not self.is_running:
            return
        
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        logger.info("Monitoring service stopped")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                await self._check_sensors()
                await self._process_alerts()
                await asyncio.sleep(settings.SENSOR_UPDATE_INTERVAL)
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(30)  # Wait before retrying
    
    async def _check_sensors(self):
        """Check sensor status and create readings"""
        db = SessionLocal()
        try:
            # Get active sensors
            sensors = db.query(Sensor).filter(Sensor.is_active == True).all()
            
            for sensor in sensors:
                try:
                    # Simulate sensor reading (replace with actual sensor communication)
                    reading_data = await self._simulate_sensor_reading(sensor)
                    
                    if reading_data:
                        # Create reading record
                        reading = SensorReading(
                            sensor_id=sensor.id,
                            value=reading_data['value'],
                            timestamp=reading_data['timestamp'],
                            quality_score=reading_data.get('quality_score', 1.0),
                            is_valid=reading_data.get('is_valid', 1)
                        )
                        db.add(reading)
                        
                        # Check for alerts
                        await self._check_sensor_thresholds(sensor, reading_data['value'], db)
                        
                except Exception as e:
                    logger.error(f"Error checking sensor {sensor.id}: {e}")
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error in sensor check: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _simulate_sensor_reading(self, sensor: Sensor) -> Dict[str, Any]:
        """Simulate sensor reading (replace with actual sensor communication)"""
        import random
        from datetime import datetime
        
        # Simulate different sensor types
        if sensor.sensor_type == "temperature":
            base_value = 25.0
            variation = 10.0
        elif sensor.sensor_type == "humidity":
            base_value = 60.0
            variation = 20.0
        elif sensor.sensor_type == "pressure":
            base_value = 1013.25
            variation = 50.0
        else:
            base_value = 50.0
            variation = 20.0
        
        # Add some randomness
        value = base_value + random.uniform(-variation, variation)
        
        # Ensure value is within sensor limits
        if sensor.min_value is not None:
            value = max(value, sensor.min_value)
        if sensor.max_value is not None:
            value = min(value, sensor.max_value)
        
        return {
            'value': round(value, 2),
            'timestamp': datetime.utcnow(),
            'quality_score': random.uniform(0.8, 1.0),
            'is_valid': 1 if random.random() > 0.05 else 0  # 5% chance of invalid reading
        }
    
    async def _check_sensor_thresholds(self, sensor: Sensor, value: float, db: Session):
        """Check if sensor value exceeds thresholds and create alerts"""
        
        # Check if there are existing active alerts for this sensor
        existing_alert = db.query(Alert).filter(
            Alert.sensor_id == sensor.id,
            Alert.status == AlertStatus.ACTIVE,
            Alert.alert_type == "threshold_exceeded"
        ).first()
        
        alert_triggered = False
        severity = AlertSeverity.MEDIUM
        
        # Check thresholds
        if sensor.alert_threshold_min is not None and value < sensor.alert_threshold_min:
            alert_triggered = True
            severity = AlertSeverity.HIGH if value < sensor.alert_threshold_min * 0.8 else AlertSeverity.MEDIUM
            title = f"Low {sensor.sensor_type} Alert"
            message = f"Sensor {sensor.name} reading ({value} {sensor.unit or ''}) is below threshold ({sensor.alert_threshold_min} {sensor.unit or ''})"
        
        elif sensor.alert_threshold_max is not None and value > sensor.alert_threshold_max:
            alert_triggered = True
            severity = AlertSeverity.HIGH if value > sensor.alert_threshold_max * 1.2 else AlertSeverity.MEDIUM
            title = f"High {sensor.sensor_type} Alert"
            message = f"Sensor {sensor.name} reading ({value} {sensor.unit or ''}) exceeds threshold ({sensor.alert_threshold_max} {sensor.unit or ''})"
        
        # Create new alert if threshold exceeded and no existing alert
        if alert_triggered and not existing_alert:
            alert = Alert(
                sensor_id=sensor.id,
                alert_type="threshold_exceeded",
                severity=severity,
                title=title,
                message=message,
                threshold_value=sensor.alert_threshold_min if value < (sensor.alert_threshold_min or 0) else sensor.alert_threshold_max,
                actual_value=value,
                triggered_at=datetime.utcnow()
            )
            db.add(alert)
            logger.warning(f"Alert created: {message}")
        
        # Resolve existing alert if value is back to normal
        elif not alert_triggered and existing_alert:
            existing_alert.status = AlertStatus.RESOLVED
            existing_alert.resolved_at = datetime.utcnow()
            logger.info(f"Alert resolved for sensor {sensor.name}")
    
    async def _process_alerts(self):
        """Process pending alerts (send notifications, etc.)"""
        db = SessionLocal()
        try:
            # Get unprocessed alerts
            alerts = db.query(Alert).filter(
                Alert.status == AlertStatus.ACTIVE,
                Alert.email_sent == False
            ).all()
            
            for alert in alerts:
                try:
                    # Send email notification
                    await self._send_alert_notification(alert)
                    alert.email_sent = True
                    
                except Exception as e:
                    logger.error(f"Error sending notification for alert {alert.id}: {e}")
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error processing alerts: {e}")
            db.rollback()
        finally:
            db.close()
    
    async def _send_alert_notification(self, alert: Alert):
        """Send alert notification (email, SMS, etc.)"""
        # TODO: Implement actual notification sending
        logger.info(f"Would send notification for alert: {alert.title}")
        
        # Example email sending (implement with actual SMTP)
        if settings.SMTP_SERVER and settings.ALERT_EMAIL_RECIPIENTS:
            # Send email logic here
            pass


# Global monitoring service instance
monitoring_service = MonitoringService()
