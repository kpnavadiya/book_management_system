"""
User-related schemas for validation and serialization.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from ..models.user import UserRole
import re


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    role: UserRole = Field(default=UserRole.MEMBER)
    
    @validator('username')
    def validate_username(cls, v):
        """Validate username format"""
        # Only alphanumeric and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        """Enforce password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "SecurePass123!",
                "role": "member"
            }
        }


class UserResponse(BaseModel):
    """Schema for user information (excludes password)"""
    id: int
    username: str
    role: UserRole
    tenant_id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
