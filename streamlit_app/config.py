"""
Configuration file for Streamlit IFC Monitoring App
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

# App Configuration
APP_TITLE = "IFC Monitoring System"
APP_ICON = "🏭"
PAGE_LAYOUT = "wide"

# Refresh intervals (in seconds)
AUTO_REFRESH_INTERVAL = 30
CHART_REFRESH_INTERVAL = 10

# Chart colors
CHART_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'warning': '#d62728',
    'danger': '#9467bd',
    'info': '#17becf'
}

# Alert severity colors
ALERT_COLORS = {
    'low': '#17becf',
    'medium': '#ff7f0e', 
    'high': '#d62728',
    'critical': '#8b0000'
}

# Sensor types configuration
SENSOR_TYPES = {
    'temperature': {
        'name': 'Temperatura',
        'unit': '°C',
        'icon': '🌡️',
        'color': '#d62728'
    },
    'humidity': {
        'name': 'Umidade',
        'unit': '%',
        'icon': '💧',
        'color': '#1f77b4'
    },
    'pressure': {
        'name': 'Pressão',
        'unit': 'hPa',
        'icon': '📊',
        'color': '#2ca02c'
    },
    'vibration': {
        'name': 'Vibração',
        'unit': 'm/s²',
        'icon': '📳',
        'color': '#ff7f0e'
    },
    'air_quality': {
        'name': 'Qualidade do Ar',
        'unit': 'ppm',
        'icon': '🌬️',
        'color': '#9467bd'
    }
}

# Default thresholds
DEFAULT_THRESHOLDS = {
    'temperature': {'min': 15, 'max': 35},
    'humidity': {'min': 30, 'max': 70},
    'pressure': {'min': 980, 'max': 1040},
    'vibration': {'min': 0, 'max': 10},
    'air_quality': {'min': 0, 'max': 100}
}
