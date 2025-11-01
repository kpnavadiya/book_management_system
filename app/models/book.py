"""
Book model representing library inventory.
Books are scoped to specific tenants.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Book(Base):
    """
    Book record within a tenant's library.
    Complete data isolation per organization.
    """
    __tablename__ = "books"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Book Information
    title = Column(String(500), nullable=False, index=True, comment="Book title")
    author = Column(String(255), nullable=False, comment="Author name")
    isbn = Column(
        String(13), 
        nullable=False, 
        index=True,
        comment="International Standard Book Number"
    )
    description = Column(Text, nullable=True, comment="Book description")
    quantity = Column(Integer, default=1, nullable=False, comment="Available copies")
    
    # Tenant Isolation
    tenant_id = Column(
        Integer, 
        ForeignKey("tenants.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Audit Trail
    created_by = Column(
        Integer, 
        ForeignKey("users.id", ondelete="SET NULL"), 
        nullable=True
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="books")
    creator = relationship("User", back_populates="books_created")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', isbn='{self.isbn}')>"
