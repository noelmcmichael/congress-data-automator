"""
Main FastAPI application for Congressional Data Automation Service.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
from .core.config import settings
from .core.database import engine, Base
from .services.congress_api import CongressApiClient

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Automated congressional data collection and API service",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import models to ensure they're registered with Base
from .models import Member, Committee, CommitteeMembership, Hearing, Witness, HearingDocument

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize API client
congress_api = CongressApiClient()


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting Congressional Data Automation Service")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down Congressional Data Automation Service")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Congressional Data Automation Service",
        "version": settings.app_version,
        "status": "active",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2025-01-04T23:35:19Z"}


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint with rate limit information."""
    rate_limit_status = congress_api.get_rate_limit_status()
    
    return {
        "api_status": "active",
        "congress_api_rate_limit": rate_limit_status,
        "database_status": "connected",
        "version": settings.app_version,
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Include API routers
from .api.v1 import data_updates
app.include_router(data_updates.router, prefix=settings.api_v1_prefix, tags=["data-updates"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )