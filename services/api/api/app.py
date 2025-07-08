"""FastAPI application for the Congressional Data API."""

from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.logging import logger, LoggingMiddleware
from .core.exceptions import APIException
from .database.connection import db_manager
from .models.base import ErrorResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Congressional Data API service")
    
    # Initialize database
    try:
        db_manager.initialize()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Congressional Data API service")
    db_manager.close()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.api_version,
        lifespan=lifespan,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    
    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # Exception handlers
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        """Handle API exceptions."""
        logger.error(
            "API exception occurred",
            path=request.url.path,
            method=request.method,
            status_code=exc.status_code,
            message=exc.message,
            detail=exc.detail,
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                message=exc.message,
                error=exc.__class__.__name__,
                detail=exc.detail,
                code=exc.status_code,
            ).dict(),
            headers=exc.headers,
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors."""
        logger.error(
            "Validation error occurred",
            path=request.url.path,
            method=request.method,
            errors=exc.errors(),
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                message="Validation error",
                error="ValidationError",
                detail=str(exc.errors()),
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            ).dict(),
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions."""
        logger.error(
            "Unexpected error occurred",
            path=request.url.path,
            method=request.method,
            error=str(exc),
            exc_info=exc,
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                message="Internal server error",
                error="InternalServerError",
                detail="An unexpected error occurred" if settings.is_production else str(exc),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ).dict(),
        )
    
    # Health check endpoint
    @app.get("/health", response_model=Dict[str, Any])
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": "congressional_data_api",
            "version": settings.api_version,
            "environment": settings.environment,
        }
    
    # Detailed health check endpoint
    @app.get("/healthz", response_model=Dict[str, Any])
    async def detailed_health_check():
        """Detailed health check endpoint."""
        db_health = db_manager.health_check()
        
        overall_status = "healthy" if db_health["status"] == "healthy" else "unhealthy"
        
        return {
            "status": overall_status,
            "service": "congressional_data_api",
            "version": settings.api_version,
            "environment": settings.environment,
            "checks": {
                "database": db_health,
            },
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Congressional Data API",
            "version": settings.api_version,
            "docs_url": "/docs" if not settings.is_production else None,
            "health_url": "/health",
        }
    
    # Include API routers
    from .endpoints.members import router as members_router
    from .endpoints.committees import router as committees_router
    from .endpoints.hearings import router as hearings_router
    from .endpoints.search import router as search_router
    
    app.include_router(members_router, prefix=settings.api_version_prefix)
    app.include_router(committees_router, prefix=settings.api_version_prefix)
    app.include_router(hearings_router, prefix=settings.api_version_prefix)
    app.include_router(search_router, prefix=settings.api_version_prefix)
    
    return app


# Create the application instance
app = create_app()