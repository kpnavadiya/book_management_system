"""
API routes module exports.
"""
from .tenants import router as tenants_router
from .auth import router as auth_router
from .books import router as books_router
from .users import router as users_router

__all__ = [
    "tenants_router",
    "auth_router",
    "books_router",
    "users_router"
]
