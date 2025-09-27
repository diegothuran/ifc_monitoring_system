"""
Pydantic schemas for authentication
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema"""
    username: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema"""
    username: str
    password: str


class UserCreate(BaseModel):
    """User creation schema"""
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: str = "viewer"


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True
