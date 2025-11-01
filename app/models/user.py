"""
User model with role-based access control.
Users belong to a specific tenant and have assigned roles.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, UniqueConstraint,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..database import Base


class UserRole(str, enum.Enum):
    """
    User permission levels within a tenant.
    
    ADMIN: Full control - manage books, users
    LIBRARIAN: Book management - create, read, update books
    MEMBER: Read-only access to books
    """
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    MEMBER = "member"


class User(Base):
    """
    User account within a specific tenant.
    Username is unique per tenant, not globally.
    """
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User Credentials
    username = Column(String(100), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False, comment="Bcrypt hashed password")
    
    # Authorization
    role = Column(
        Enum(UserRole), 
        nullable=False, 
        default=UserRole.MEMBER,
        comment="User's permission level"
    )
    
    # Tenant Association
    tenant_id = Column(
        Integer, 
        ForeignKey("tenants.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Status
    is_active = Column(Boolean, default=True, comment="Whether user account is active")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    books_created = relationship("Book", back_populates="creator", lazy="dynamic")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('username', 'tenant_id', name='unique_username_per_tenant'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"
