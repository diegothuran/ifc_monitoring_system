"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./ifc_monitoring.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "IFC Monitoring System"
    
    # Sensor Configuration
    SENSOR_UPDATE_INTERVAL: int = 60  # seconds
    ALERT_THRESHOLD_TEMPERATURE: float = 80.0  # celsius
    ALERT_THRESHOLD_HUMIDITY: float = 90.0  # percentage
    ALERT_THRESHOLD_PRESSURE: float = 1013.25  # hPa
    
    # Email Configuration
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    ALERT_EMAIL_RECIPIENTS: List[str] = []
    
    # Development/Production
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Heroku specific
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
