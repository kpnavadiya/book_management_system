"""
Application configuration management.
Loads settings from environment variables for security.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Centralized configuration for the application.
    All sensitive data should be in .env file.
    """
    # Application Metadata
    PROJECT_NAME: str = "Multi-Tenant Book Management System"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Enterprise-grade multi-tenant book management with RBAC"
    API_V1_PREFIX: str = "/api"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://bookuser:password@localhost/bookdb"
    DATABASE_ECHO: bool = False  # Set True for SQL query logging
    
    # JWT Security Settings
    SECRET_KEY: str = "change-this-secret-key-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Multi-Tenancy Configuration
    BASE_DOMAIN: str = "localhost"
    TENANT_URL_PATTERN: str = "subdomain"  # Options: "subdomain" or "path"
    
    # Security Settings
    ALLOWED_HOSTS: list = ["*"]
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173"
    ]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
