#!/usr/bin/env python3
"""
Script to create sample data for the IFC Monitoring System
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.core.database import SessionLocal, engine
from backend.models import Base, User, Location, Sensor, SensorReading, Alert
from backend.models.user import UserRole
from backend.models.alert import AlertSeverity, AlertStatus
from backend.auth.security import get_password_hash

def create_sample_data():
    """Create sample data for testing"""
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create sample users
        print("Creating sample users...")
        
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@company.com",
                full_name="System Administrator",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN,
                is_active=True,
                is_superuser=True
            )
            db.add(admin_user)
        
        # Create operator user
        operator_user = db.query(User).filter(User.username == "operator").first()
        if not operator_user:
            operator_user = User(
                username="operator",
                email="operator@company.com",
                full_name="System Operator",
                hashed_password=get_password_hash("operator123"),
                role=UserRole.OPERATOR,
                is_active=True
            )
            db.add(operator_user)
        
        # Create viewer user
        viewer_user = db.query(User).filter(User.username == "viewer").first()
        if not viewer_user:
            viewer_user = User(
                username="viewer",
                email="viewer@company.com",
                full_name="System Viewer",
                hashed_password=get_password_hash("viewer123"),
                role=UserRole.VIEWER,
                is_active=True
            )
            db.add(viewer_user)
        
        db.commit()
        print("✓ Users created successfully")
        
        # Create sample locations
        print("Creating sample locations...")
        
        locations_data = [
            {
                "name": "Main Building - Floor 1",
                "description": "Main office building, first floor",
                "building": "Main Building",
                "floor": "1",
                "room": "Office Area",
                "zone": "Administrative",
                "responsible_person": "John Smith",
                "phone": "+1-555-0101",
                "email": "john.smith@company.com"
            },
            {
                "name": "Main Building - Floor 2",
                "description": "Main office building, second floor",
                "building": "Main Building",
                "floor": "2",
                "room": "Conference Room",
                "zone": "Meeting",
                "responsible_person": "Jane Doe",
                "phone": "+1-555-0102",
                "email": "jane.doe@company.com"
            },
            {
                "name": "Warehouse A",
                "description": "Main storage warehouse",
                "building": "Warehouse A",
                "floor": "Ground",
                "room": "Storage Area",
                "zone": "Storage",
                "responsible_person": "Mike Johnson",
                "phone": "+1-555-0103",
                "email": "mike.johnson@company.com"
            },
            {
                "name": "Production Floor",
                "description": "Manufacturing production area",
                "building": "Production Building",
                "floor": "Ground",
                "room": "Production Line",
                "zone": "Manufacturing",
                "responsible_person": "Sarah Wilson",
                "phone": "+1-555-0104",
                "email": "sarah.wilson@company.com"
            },
            {
                "name": "Server Room",
                "description": "Data center and server room",
                "building": "Main Building",
                "floor": "Basement",
                "room": "Server Room",
                "zone": "IT Infrastructure",
                "responsible_person": "David Brown",
                "phone": "+1-555-0105",
                "email": "david.brown@company.com"
            }
        ]
        
        locations = []
        for loc_data in locations_data:
            location = db.query(Location).filter(Location.name == loc_data["name"]).first()
            if not location:
                location = Location(**loc_data)
                db.add(location)
                locations.append(location)
            else:
                locations.append(location)
        
        db.commit()
        print("✓ Locations created successfully")
        
        # Create sample sensors
        print("Creating sample sensors...")
        
        sensors_data = [
            {
                "name": "Temperature Sensor - Office 1",
                "sensor_type": "temperature",
                "location_id": locations[0].id,
                "device_id": "TEMP-001",
                "model": "DS18B20",
                "manufacturer": "Maxim Integrated",
                "serial_number": "TEMP001-SN-2023",
                "min_value": -40.0,
                "max_value": 85.0,
                "unit": "°C",
                "update_interval": 60,
                "alert_threshold_min": 15.0,
                "alert_threshold_max": 30.0,
                "description": "Digital temperature sensor for office monitoring",
                "installation_date": datetime.utcnow() - timedelta(days=30)
            },
            {
                "name": "Humidity Sensor - Office 1",
                "sensor_type": "humidity",
                "location_id": locations[0].id,
                "device_id": "HUM-001",
                "model": "SHT30",
                "manufacturer": "Sensirion",
                "serial_number": "HUM001-SN-2023",
                "min_value": 0.0,
                "max_value": 100.0,
                "unit": "%",
                "update_interval": 60,
                "alert_threshold_min": 30.0,
                "alert_threshold_max": 70.0,
                "description": "Digital humidity sensor for office monitoring",
                "installation_date": datetime.utcnow() - timedelta(days=30)
            },
            {
                "name": "Pressure Sensor - Conference Room",
                "sensor_type": "pressure",
                "location_id": locations[1].id,
                "device_id": "PRES-001",
                "model": "BMP280",
                "manufacturer": "Bosch",
                "serial_number": "PRES001-SN-2023",
                "min_value": 300.0,
                "max_value": 1100.0,
                "unit": "hPa",
                "update_interval": 60,
                "alert_threshold_min": 950.0,
                "alert_threshold_max": 1050.0,
                "description": "Barometric pressure sensor for conference room",
                "installation_date": datetime.utcnow() - timedelta(days=25)
            },
            {
                "name": "Temperature Sensor - Warehouse",
                "sensor_type": "temperature",
                "location_id": locations[2].id,
                "device_id": "TEMP-002",
                "model": "DS18B20",
                "manufacturer": "Maxim Integrated",
                "serial_number": "TEMP002-SN-2023",
                "min_value": -40.0,
                "max_value": 85.0,
                "unit": "°C",
                "update_interval": 120,
                "alert_threshold_min": 5.0,
                "alert_threshold_max": 25.0,
                "description": "Digital temperature sensor for warehouse monitoring",
                "installation_date": datetime.utcnow() - timedelta(days=20)
            },
            {
                "name": "Temperature Sensor - Production Floor",
                "sensor_type": "temperature",
                "location_id": locations[3].id,
                "device_id": "TEMP-003",
                "model": "DS18B20",
                "manufacturer": "Maxim Integrated",
                "serial_number": "TEMP003-SN-2023",
                "min_value": -40.0,
                "max_value": 85.0,
                "unit": "°C",
                "update_interval": 30,
                "alert_threshold_min": 18.0,
                "alert_threshold_max": 28.0,
                "description": "Digital temperature sensor for production floor",
                "installation_date": datetime.utcnow() - timedelta(days=15)
            },
            {
                "name": "Temperature Sensor - Server Room",
                "sensor_type": "temperature",
                "location_id": locations[4].id,
                "device_id": "TEMP-004",
                "model": "DS18B20",
                "manufacturer": "Maxim Integrated",
                "serial_number": "TEMP004-SN-2023",
                "min_value": -40.0,
                "max_value": 85.0,
                "unit": "°C",
                "update_interval": 30,
                "alert_threshold_min": 18.0,
                "alert_threshold_max": 24.0,
                "description": "Critical temperature sensor for server room",
                "installation_date": datetime.utcnow() - timedelta(days=10)
            },
            {
                "name": "Humidity Sensor - Server Room",
                "sensor_type": "humidity",
                "location_id": locations[4].id,
                "device_id": "HUM-002",
                "model": "SHT30",
                "manufacturer": "Sensirion",
                "serial_number": "HUM002-SN-2023",
                "min_value": 0.0,
                "max_value": 100.0,
                "unit": "%",
                "update_interval": 30,
                "alert_threshold_min": 40.0,
                "alert_threshold_max": 60.0,
                "description": "Critical humidity sensor for server room",
                "installation_date": datetime.utcnow() - timedelta(days=10)
            }
        ]
        
        sensors = []
        for sensor_data in sensors_data:
            sensor = db.query(Sensor).filter(Sensor.device_id == sensor_data["device_id"]).first()
            if not sensor:
                sensor = Sensor(**sensor_data)
                db.add(sensor)
                sensors.append(sensor)
            else:
                sensors.append(sensor)
        
        db.commit()
        print("✓ Sensors created successfully")
        
        # Create sample readings
        print("Creating sample readings...")
        
        import random
        from datetime import datetime, timedelta
        
        # Generate readings for the last 7 days
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=7)
        
        for sensor in sensors:
            # Generate readings every hour for the last 7 days
            current_time = start_time
            while current_time <= end_time:
                # Generate realistic sensor values based on sensor type
                if sensor.sensor_type == "temperature":
                    base_value = 22.0
                    variation = 5.0
                    if "Server Room" in sensor.name:
                        base_value = 20.0
                        variation = 2.0
                    elif "Warehouse" in sensor.name:
                        base_value = 15.0
                        variation = 3.0
                elif sensor.sensor_type == "humidity":
                    base_value = 50.0
                    variation = 15.0
                elif sensor.sensor_type == "pressure":
                    base_value = 1013.25
                    variation = 20.0
                else:
                    base_value = 50.0
                    variation = 10.0
                
                value = base_value + random.uniform(-variation, variation)
                
                # Ensure value is within sensor limits
                if sensor.min_value is not None:
                    value = max(value, sensor.min_value)
                if sensor.max_value is not None:
                    value = min(value, sensor.max_value)
                
                reading = SensorReading(
                    sensor_id=sensor.id,
                    value=round(value, 2),
                    timestamp=current_time,
                    quality_score=random.uniform(0.9, 1.0),
                    is_valid=1 if random.random() > 0.02 else 0  # 2% chance of invalid reading
                )
                db.add(reading)
                
                current_time += timedelta(hours=1)
        
        db.commit()
        print("✓ Sample readings created successfully")
        
        # Create sample alerts
        print("Creating sample alerts...")
        
        # Create some active alerts
        alert_data = [
            {
                "sensor_id": sensors[5].id,  # Server room temperature
                "alert_type": "threshold_exceeded",
                "severity": AlertSeverity.HIGH,
                "status": AlertStatus.ACTIVE,
                "title": "High Temperature Alert - Server Room",
                "message": f"Temperature sensor {sensors[5].name} reading (28.5°C) exceeds threshold (24.0°C)",
                "threshold_value": 24.0,
                "actual_value": 28.5,
                "triggered_at": datetime.utcnow() - timedelta(hours=2)
            },
            {
                "sensor_id": sensors[3].id,  # Warehouse temperature
                "alert_type": "threshold_exceeded",
                "severity": AlertSeverity.MEDIUM,
                "status": AlertStatus.ACTIVE,
                "title": "Low Temperature Alert - Warehouse",
                "message": f"Temperature sensor {sensors[3].name} reading (3.2°C) is below threshold (5.0°C)",
                "threshold_value": 5.0,
                "actual_value": 3.2,
                "triggered_at": datetime.utcnow() - timedelta(hours=1)
            }
        ]
        
        for alert_info in alert_data:
            alert = Alert(**alert_info)
            db.add(alert)
        
        # Create some resolved alerts
        resolved_alert_data = [
            {
                "sensor_id": sensors[0].id,  # Office temperature
                "alert_type": "threshold_exceeded",
                "severity": AlertSeverity.MEDIUM,
                "status": AlertStatus.RESOLVED,
                "title": "High Temperature Alert - Office",
                "message": f"Temperature sensor {sensors[0].name} reading (32.1°C) exceeded threshold (30.0°C)",
                "threshold_value": 30.0,
                "actual_value": 32.1,
                "triggered_at": datetime.utcnow() - timedelta(days=1),
                "resolved_at": datetime.utcnow() - timedelta(hours=12),
                "acknowledged_by": operator_user.id
            }
        ]
        
        for alert_info in resolved_alert_data:
            alert = Alert(**alert_info)
            db.add(alert)
        
        db.commit()
        print("✓ Sample alerts created successfully")
        
        print("\n" + "="*50)
        print("SAMPLE DATA CREATION COMPLETED!")
        print("="*50)
        print("\nDefault login credentials:")
        print("Admin: admin / admin123")
        print("Operator: operator / operator123")
        print("Viewer: viewer / viewer123")
        print("\nCreated:")
        print(f"- {len(locations)} locations")
        print(f"- {len(sensors)} sensors")
        print("- Sample readings for the last 7 days")
        print("- Sample alerts (active and resolved)")
        print("\nYou can now start the system with: python main.py")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
