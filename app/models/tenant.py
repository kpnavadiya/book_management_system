"""
Tenant (Organization) model.
Represents independent organizations using the system.
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Tenant(Base):
    """
    Organization/Company using the book management system.
    Each tenant has complete data isolation.
    """
    __tablename__ = "tenants"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Organization Details
    name = Column(String(255), nullable=False, comment="Organization name")
    subdomain = Column(
        String(63), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="Unique subdomain identifier (e.g., 'acme')"
    )
    
    # Status
    is_active = Column(Boolean, default=True, comment="Whether tenant is active")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (One tenant has many users and books)
    users = relationship(
        "User", 
        back_populates="tenant", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    books = relationship(
        "Book", 
        back_populates="tenant", 
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, name='{self.name}', subdomain='{self.subdomain}')>"
