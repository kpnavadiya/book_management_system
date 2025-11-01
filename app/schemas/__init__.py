"""
Schema exports for easy imports.
"""
from .auth import LoginRequest, Token, TokenPayload, RefreshTokenRequest, ChangePasswordRequest
from .tenant import TenantCreate, TenantResponse, TenantUpdate
from .user import UserCreate, UserResponse, UserUpdate
from .book import BookCreate, BookUpdate, BookResponse

__all__ = [
    # Auth
    "LoginRequest", "Token", "TokenPayload", "RefreshTokenRequest", "ChangePasswordRequest",
    # Tenant
    "TenantCreate", "TenantResponse", "TenantUpdate",
    # User
    "UserCreate", "UserResponse", "UserUpdate",
    # Book
    "BookCreate", "BookUpdate", "BookResponse"
]
