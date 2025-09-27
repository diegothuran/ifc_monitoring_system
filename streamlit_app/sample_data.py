"""
Sample data generator for IFC Monitoring System
Useful for testing and demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_sample_sensors():
    """Generate sample sensor data"""
    sensors = [
        {
            "id": 1,
            "name": "Temperatura Sala 101",
            "sensor_type": "temperature",
            "device_id": "TEMP-001",
            "location_id": 1,
            "model": "DS18B20",
            "manufacturer": "Maxim Integrated",
            "unit": "°C",
            "is_active": True,
            "update_interval": 60,
            "alert_threshold_min": 15.0,
            "alert_threshold_max": 35.0,
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "id": 2,
            "name": "Umidade Sala 101",
            "sensor_type": "humidity",
            "device_id": "HUM-001",
            "location_id": 1,
            "model": "DHT22",
            "manufacturer": "Aosong",
            "unit": "%",
            "is_active": True,
            "update_interval": 60,
            "alert_threshold_min": 30.0,
            "alert_threshold_max": 70.0,
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "id": 3,
            "name": "Pressão Atmosférica",
            "sensor_type": "pressure",
            "device_id": "PRESS-001",
            "location_id": 2,
            "model": "BMP280",
            "manufacturer": "Bosch",
            "unit": "hPa",
            "is_active": True,
            "update_interval": 300,
            "alert_threshold_min": 980.0,
            "alert_threshold_max": 1040.0,
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "id": 4,
            "name": "Vibração Motor 1",
            "sensor_type": "vibration",
            "device_id": "VIB-001",
            "location_id": 3,
            "model": "ADXL345",
            "manufacturer": "Analog Devices",
            "unit": "m/s²",
            "is_active": True,
            "update_interval": 30,
            "alert_threshold_min": 0.0,
            "alert_threshold_max": 10.0,
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "id": 5,
            "name": "Qualidade do Ar",
            "sensor_type": "air_quality",
            "device_id": "AIR-001",
            "location_id": 1,
            "model": "MQ-135",
            "manufacturer": "Winsen",
            "unit": "ppm",
            "is_active": True,
            "update_interval": 120,
            "alert_threshold_min": 0.0,
            "alert_threshold_max": 100.0,
            "created_at": "2024-01-15T10:00:00Z"
        }
    ]
    return sensors

def generate_sample_locations():
    """Generate sample location data"""
    locations = [
        {
            "id": 1,
            "name": "Sala de Controle Principal",
            "description": "Sala principal de controle do sistema",
            "building": "Edifício A",
            "floor": "1º Andar",
            "room": "101",
            "zone": "Controle",
            "responsible_person": "João Silva",
            "phone": "(11) 99999-1111",
            "email": "joao.silva@company.com",
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "id": 2,
            "name": "Área de Produção",
            "description": "Área principal de produção",
            "building": "Edifício B",
            "floor": "Térreo",
            "room": "200",
            "zone": "Produção",
            "responsible_person": "Maria Santos",
            "phone": "(11) 99999-2222",
            "email": "maria.santos@company.com",
            "created_at": "2024-01-15T10:00:00Z"
        },
        {
            "id": 3,
            "name": "Sala de Máquinas",
            "description": "Sala com equipamentos principais",
            "building": "Edifício C",
            "floor": "Subsolo",
            "room": "001",
            "zone": "Máquinas",
            "responsible_person": "Pedro Oliveira",
            "phone": "(11) 99999-3333",
            "email": "pedro.oliveira@company.com",
            "created_at": "2024-01-15T10:00:00Z"
        }
    ]
    return locations

def generate_sample_readings(days=7, sensor_id=1):
    """Generate sample sensor readings"""
    readings = []
    start_time = datetime.now() - timedelta(days=days)
    
    # Different patterns for different sensor types
    sensor_patterns = {
        1: {"base": 25, "amplitude": 10, "trend": 0},  # temperature
        2: {"base": 60, "amplitude": 20, "trend": 0},  # humidity
        3: {"base": 1013, "amplitude": 50, "trend": 0}, # pressure
        4: {"base": 2, "amplitude": 5, "trend": 0.1},   # vibration
        5: {"base": 50, "amplitude": 30, "trend": 0}    # air quality
    }
    
    pattern = sensor_patterns.get(sensor_id, {"base": 50, "amplitude": 20, "trend": 0})
    
    for i in range(days * 24 * 4):  # 4 readings per hour
        timestamp = start_time + timedelta(minutes=15 * i)
        
        # Generate value with pattern
        hour_of_day = timestamp.hour
        day_of_week = timestamp.weekday()
        
        # Daily cycle
        daily_cycle = np.sin(2 * np.pi * hour_of_day / 24) * pattern["amplitude"] / 2
        
        # Weekly trend
        weekly_trend = pattern["trend"] * day_of_week
        
        # Random noise
        noise = random.gauss(0, pattern["amplitude"] * 0.1)
        
        value = pattern["base"] + daily_cycle + weekly_trend + noise
        
        # Add some outliers occasionally
        if random.random() < 0.02:  # 2% chance of outlier
            value += random.gauss(0, pattern["amplitude"] * 0.5)
        
        readings.append({
            "id": len(readings) + 1,
            "sensor_id": sensor_id,
            "value": round(value, 2),
            "timestamp": timestamp.isoformat() + "Z",
            "quality_score": random.uniform(0.8, 1.0),
            "is_valid": 1 if random.random() > 0.05 else 0
        })
    
    return readings

def generate_sample_alerts():
    """Generate sample alert data"""
    alerts = [
        {
            "id": 1,
            "sensor_id": 1,
            "alert_type": "threshold_exceeded",
            "severity": "high",
            "status": "active",
            "title": "Temperatura Alta Detectada",
            "message": "Sensor TEMP-001 registrou temperatura acima do limite (32.5°C > 35°C)",
            "threshold_value": 35.0,
            "actual_value": 32.5,
            "triggered_at": "2024-01-20T14:30:00Z",
            "created_at": "2024-01-20T14:30:00Z"
        },
        {
            "id": 2,
            "sensor_id": 2,
            "alert_type": "threshold_exceeded",
            "severity": "medium",
            "status": "acknowledged",
            "title": "Umidade Elevada",
            "message": "Sensor HUM-001 registrou umidade acima do normal (75% > 70%)",
            "threshold_value": 70.0,
            "actual_value": 75.0,
            "triggered_at": "2024-01-20T12:15:00Z",
            "acknowledged_at": "2024-01-20T12:30:00Z",
            "acknowledged_by": 1,
            "created_at": "2024-01-20T12:15:00Z"
        },
        {
            "id": 3,
            "sensor_id": 4,
            "alert_type": "threshold_exceeded",
            "severity": "critical",
            "status": "resolved",
            "title": "Vibração Crítica",
            "message": "Sensor VIB-001 detectou vibração crítica no motor (12.3 m/s² > 10 m/s²)",
            "threshold_value": 10.0,
            "actual_value": 12.3,
            "triggered_at": "2024-01-19T16:45:00Z",
            "resolved_at": "2024-01-19T17:00:00Z",
            "created_at": "2024-01-19T16:45:00Z"
        }
    ]
    return alerts

def create_sample_dashboard_data():
    """Create complete sample data for dashboard"""
    return {
        "sensors": {
            "total": 5,
            "active": 5,
            "inactive": 0,
            "data": generate_sample_sensors()
        },
        "alerts": {
            "total": 3,
            "active": 1,
            "acknowledged": 1,
            "resolved": 1,
            "data": generate_sample_alerts()
        },
        "locations": {
            "total": 3,
            "data": generate_sample_locations()
        },
        "readings": {
            "today": 240,
            "data": generate_sample_readings(days=1, sensor_id=1)
        }
    }

if __name__ == "__main__":
    # Generate and print sample data
    print("Sample Sensors:")
    for sensor in generate_sample_sensors():
        print(f"  {sensor['name']} ({sensor['sensor_type']})")
    
    print("\nSample Locations:")
    for location in generate_sample_locations():
        print(f"  {location['name']} - {location['building']}")
    
    print("\nSample Alerts:")
    for alert in generate_sample_alerts():
        print(f"  {alert['title']} - {alert['severity']}")
