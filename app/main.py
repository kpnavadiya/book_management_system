"""
Main FastAPI application.
Configures middleware, routes, and startup events.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .config import settings
from .database import init_db
from .routes import tenants_router, auth_router, books_router, users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Runs on startup and shutdown.
    """
    # Startup: Initialize database
    print("🚀 Starting application...")
    init_db()
    print("✅ Database initialized")
    # Print the running URL info explicitly
    print("ℹ️ Application running at http://0.0.0.0:8000")
    host = "http://localhost:8000"  # Change if your host or port differ
    prefix = settings.API_V1_PREFIX

    print(f"👾 API Docs: {host}{prefix}/docs")
    print(f"📜 OpenAPI JSON: {host}{prefix}/openapi.json")
    print(f"📚 Redoc Docs: {host}{prefix}/redoc")
    print(f"⚙️  Health Check: {host}/health")
    print(f"🏠  Root Endpoint: {host}/")

    yield
    
    # Shutdown
    print("👋 Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    lifespan=lifespan
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


# Include routers
app.include_router(tenants_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(books_router, prefix=settings.API_V1_PREFIX)
app.include_router(users_router, prefix=settings.API_V1_PREFIX)


# Root endpoint
@app.get("/")
def root():
    """
    Welcome endpoint with API information.
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "documentation": f"{settings.API_V1_PREFIX}/docs",
        "health_check": "/health"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DATABASE_ECHO else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI application at http://0.0.0.0:8000")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
