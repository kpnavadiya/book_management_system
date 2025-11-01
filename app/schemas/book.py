"""
Book-related schemas for validation and serialization.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class BookCreate(BaseModel):
    """Schema for adding a new book"""
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=255)
    isbn: str = Field(..., min_length=10, max_length=13)
    description: Optional[str] = Field(None, max_length=2000)
    quantity: int = Field(default=1, ge=0, description="Number of copies")
    
    @validator('title', 'author')
    def validate_not_empty(cls, v):
        """Ensure fields are not just whitespace"""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or only whitespace')
        return v.strip()
    
    @validator('isbn')
    def validate_isbn(cls, v):
        """Validate ISBN format (10 or 13 digits)"""
        # Remove hyphens and spaces
        isbn = v.replace('-', '').replace(' ', '').strip()
        
        # Must be digits only
        if not isbn.isdigit():
            raise ValueError('ISBN must contain only digits (hyphens/spaces will be removed)')
        
        # Must be 10 or 13 digits
        if len(isbn) not in [10, 13]:
            raise ValueError('ISBN must be 10 or 13 digits')
        
        return isbn
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "isbn": "978-0743273565",
                "description": "A classic American novel",
                "quantity": 5
            }
        }


class BookUpdate(BaseModel):
    """Schema for updating book information"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    description: Optional[str] = Field(None, max_length=2000)
    quantity: Optional[int] = Field(None, ge=0)


class BookResponse(BaseModel):
    """Schema for book information returned to client"""
    id: int
    title: str
    author: str
    isbn: str
    description: Optional[str]
    quantity: int
    tenant_id: int
    created_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
