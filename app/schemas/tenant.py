"""
Tenant-related schemas for validation and serialization.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
import re
from typing import Optional

class TenantCreate(BaseModel):
    """Schema for creating a new tenant"""
    name: str = Field(..., min_length=3, max_length=255, description="Organization name")
    subdomain: str = Field(..., min_length=3, max_length=63, description="Unique subdomain")
    
    @validator('subdomain')
    def validate_subdomain(cls, v):
        """Ensure subdomain is DNS-compliant"""
        # Only lowercase letters, numbers, hyphens
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Subdomain must contain only lowercase letters, numbers, and hyphens')
        
        # Cannot start or end with hyphen
        if v.startswith('-') or v.endswith('-'):
            raise ValueError('Subdomain cannot start or end with hyphen')
        
        # Reserved subdomains
        reserved = ['www', 'api', 'admin', 'app', 'mail', 'ftp', 'localhost']
        if v in reserved:
            raise ValueError(f'Subdomain "{v}" is reserved')
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Acme Corporation Library",
                "subdomain": "acme"
            }
        }


class TenantResponse(BaseModel):
    """Schema for tenant information returned to client"""
    id: int
    name: str
    subdomain: str
    is_active: bool
    created_at: datetime
    url: str
    
    class Config:
        from_attributes = True


class TenantUpdate(BaseModel):
    """Schema for updating tenant information"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    is_active: Optional[bool] = None
