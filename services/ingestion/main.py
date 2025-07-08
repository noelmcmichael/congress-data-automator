"""
Congressional Data Ingestion Service

Enterprise-grade FastAPI application for collecting and staging congressional data.
This service handles data collection from multiple sources and prepares it for
validation and promotion to production.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import structlog

from ingestion.core.config import settings, validate_configuration
from ingestion.core.logging import setup_logging
from ingestion.core.database import get_db, health_check, create_staging_tables, engine
from ingestion.processors.data_processor import DataProcessor


# Initialize logging
logger = setup_logging()

# Validate configuration on startup
try:
    validate_configuration()
except ValueError as e:
    logger.error("Configuration validation failed", error=str(e))
    raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown tasks."""
    # Startup
    logger.info(
        "Starting Congressional Data Ingestion Service",
        version=settings.app_version,
        environment=settings.environment
    )
    
    try:
        # Create staging tables
        create_staging_tables()
        logger.info("Staging tables initialized")
        
        # Initialize data processor
        app.state.data_processor = DataProcessor()
        logger.info("Data processor initialized")
        
    except Exception as e:
        logger.error("Startup failed", error=str(e), exc_info=e)
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Congressional Data Ingestion Service")


# Create FastAPI application
app = FastAPI(
    title="Congressional Data Ingestion Service",
    description="Enterprise-grade data collection and staging for congressional information",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with service information."""
    return {
        "service": "Congressional Data Ingestion Service",
        "version": settings.app_version,
        "environment": settings.environment,
        "status": "active",
        "docs_url": "/docs"
    }


@app.get("/healthz")
async def health_check_endpoint() -> Dict[str, Any]:
    """
    Health check endpoint for container orchestration.
    
    Returns service health status including database connectivity.
    """
    try:
        # Check database connectivity
        db_healthy = health_check()
        
        health_status = {
            "status": "healthy" if db_healthy else "unhealthy",
            "service": "congressional-ingestion",
            "version": settings.app_version,
            "database": "connected" if db_healthy else "disconnected",
            "timestamp": "2025-01-08T20:00:00Z"
        }
        
        status_code = 200 if db_healthy else 503
        return JSONResponse(content=health_status, status_code=status_code)
        
    except Exception as e:
        logger.error("Health check failed", error=str(e), exc_info=e)
        return JSONResponse(
            content={
                "status": "unhealthy",
                "service": "congressional-ingestion",
                "error": str(e)
            },
            status_code=503
        )


@app.get("/metrics")
async def metrics_endpoint() -> Dict[str, Any]:
    """
    Metrics endpoint for monitoring and observability.
    
    Returns basic service metrics for Prometheus or other monitoring systems.
    """
    # TODO: Implement Prometheus metrics collection
    return {
        "service": "congressional-ingestion",
        "version": settings.app_version,
        "uptime": "placeholder",
        "requests_total": "placeholder",
        "errors_total": "placeholder"
    }


@app.post("/ingest/members")
async def ingest_members(
    background_tasks: BackgroundTasks,
    current_only: bool = True,
    truncate_staging: bool = True,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Ingest congressional members data.
    
    Args:
        current_only: Only collect current members (default: True)
        truncate_staging: Truncate staging table before ingestion (default: True)
        
    Returns:
        Dict with operation status and metadata
    """
    logger.info(
        "Members ingestion requested",
        current_only=current_only,
        truncate_staging=truncate_staging
    )
    
    try:
        # Run processing in background for large datasets
        background_tasks.add_task(
            _process_members_task,
            current_only=current_only,
            truncate_staging=truncate_staging
        )
        
        return {
            "status": "accepted",
            "operation": "ingest_members",
            "message": "Members ingestion started in background",
            "parameters": {
                "current_only": current_only,
                "truncate_staging": truncate_staging
            }
        }
        
    except Exception as e:
        logger.error("Members ingestion failed", error=str(e), exc_info=e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start members ingestion: {str(e)}"
        )


@app.post("/ingest/committees")
async def ingest_committees(
    background_tasks: BackgroundTasks,
    truncate_staging: bool = True,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Ingest congressional committees data.
    
    Args:
        truncate_staging: Truncate staging table before ingestion (default: True)
        
    Returns:
        Dict with operation status and metadata
    """
    logger.info(
        "Committees ingestion requested",
        truncate_staging=truncate_staging
    )
    
    try:
        background_tasks.add_task(
            _process_committees_task,
            truncate_staging=truncate_staging
        )
        
        return {
            "status": "accepted",
            "operation": "ingest_committees",
            "message": "Committees ingestion started in background",
            "parameters": {
                "truncate_staging": truncate_staging
            }
        }
        
    except Exception as e:
        logger.error("Committees ingestion failed", error=str(e), exc_info=e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start committees ingestion: {str(e)}"
        )


@app.post("/ingest/hearings")
async def ingest_hearings(
    background_tasks: BackgroundTasks,
    days_back: int = 30,
    include_web_scraping: bool = True,
    truncate_staging: bool = True,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Ingest congressional hearings data.
    
    Args:
        days_back: Number of days to look back for hearings (default: 30)
        include_web_scraping: Include web scraping sources (default: True)
        truncate_staging: Truncate staging table before ingestion (default: True)
        
    Returns:
        Dict with operation status and metadata
    """
    logger.info(
        "Hearings ingestion requested",
        days_back=days_back,
        include_web_scraping=include_web_scraping,
        truncate_staging=truncate_staging
    )
    
    try:
        background_tasks.add_task(
            _process_hearings_task,
            days_back=days_back,
            include_web_scraping=include_web_scraping,
            truncate_staging=truncate_staging
        )
        
        return {
            "status": "accepted",
            "operation": "ingest_hearings",
            "message": "Hearings ingestion started in background",
            "parameters": {
                "days_back": days_back,
                "include_web_scraping": include_web_scraping,
                "truncate_staging": truncate_staging
            }
        }
        
    except Exception as e:
        logger.error("Hearings ingestion failed", error=str(e), exc_info=e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start hearings ingestion: {str(e)}"
        )


# Background task functions
async def _process_members_task(current_only: bool, truncate_staging: bool) -> None:
    """Background task for processing members."""
    try:
        # Get fresh database session for background task
        from ingestion.core.database import SessionLocal
        db = SessionLocal()
        
        try:
            processor = DataProcessor()
            result = await processor.process_members(
                session=db,
                current_only=current_only,
                truncate_staging=truncate_staging
            )
            
            logger.info(
                "Members processing completed",
                success=result.success,
                records_processed=result.records_processed,
                records_inserted=result.records_inserted,
                errors=len(result.errors)
            )
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error("Members background task failed", error=str(e), exc_info=e)


async def _process_committees_task(truncate_staging: bool) -> None:
    """Background task for processing committees."""
    try:
        from ingestion.core.database import SessionLocal
        db = SessionLocal()
        
        try:
            processor = DataProcessor()
            result = await processor.process_committees(
                session=db,
                truncate_staging=truncate_staging
            )
            
            logger.info(
                "Committees processing completed",
                success=result.success,
                records_processed=result.records_processed,
                records_inserted=result.records_inserted,
                errors=len(result.errors)
            )
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error("Committees background task failed", error=str(e), exc_info=e)


async def _process_hearings_task(
    days_back: int, 
    include_web_scraping: bool, 
    truncate_staging: bool
) -> None:
    """Background task for processing hearings."""
    try:
        from ingestion.core.database import SessionLocal
        db = SessionLocal()
        
        try:
            processor = DataProcessor()
            result = await processor.process_hearings(
                session=db,
                days_back=days_back,
                include_web_scraping=include_web_scraping,
                truncate_staging=truncate_staging
            )
            
            logger.info(
                "Hearings processing completed",
                success=result.success,
                records_processed=result.records_processed,
                records_inserted=result.records_inserted,
                errors=len(result.errors)
            )
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error("Hearings background task failed", error=str(e), exc_info=e)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(
        "Unhandled exception",
        path=request.url.path,
        method=request.method,
        error_type=type(exc).__name__,
        error_message=str(exc),
        exc_info=exc
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "service": "congressional-ingestion",
            "path": request.url.path
        }
    )


if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT environment variable for Cloud Run compatibility
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )