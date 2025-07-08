"""Monitoring and health check endpoints."""

import os
import time
import psutil
from datetime import datetime, timezone
from typing import Dict, Any, List

from fastapi import APIRouter, Depends, status
from sqlalchemy import text

from ..core.config import settings
from ..core.logging import logger
from ..database.connection import db_manager
from ..models.base import BaseResponse

router = APIRouter(tags=["monitoring"])


def get_system_metrics() -> Dict[str, Any]:
    """Get system performance metrics."""
    try:
        process = psutil.Process()
        
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_usage": {
                "percent": psutil.virtual_memory().percent,
                "available_mb": psutil.virtual_memory().available / 1024 / 1024,
                "total_mb": psutil.virtual_memory().total / 1024 / 1024,
            },
            "process": {
                "memory_mb": process.memory_info().rss / 1024 / 1024,
                "cpu_percent": process.cpu_percent(),
                "threads": process.num_threads(),
                "open_files": len(process.open_files()),
            },
            "disk_usage": {
                "percent": psutil.disk_usage("/").percent,
                "free_gb": psutil.disk_usage("/").free / 1024 / 1024 / 1024,
                "total_gb": psutil.disk_usage("/").total / 1024 / 1024 / 1024,
            }
        }
    except Exception as e:
        logger.error(f"Error getting system metrics: {e}")
        return {"error": str(e)}


def check_database_health() -> Dict[str, Any]:
    """Check database health and performance."""
    start_time = time.time()
    
    try:
        # Get database session
        with db_manager.get_session() as session:
            # Simple query to test connectivity
            result = session.execute(text("SELECT 1 as test"))
            test_value = result.scalar()
            
            # Check table counts
            member_count = session.execute(text("SELECT COUNT(*) FROM members")).scalar()
            committee_count = session.execute(text("SELECT COUNT(*) FROM committees")).scalar()
            hearing_count = session.execute(text("SELECT COUNT(*) FROM hearings")).scalar()
            
            query_time = (time.time() - start_time) * 1000  # Convert to ms
            
            return {
                "status": "healthy" if test_value == 1 else "unhealthy",
                "response_time_ms": round(query_time, 2),
                "table_counts": {
                    "members": member_count,
                    "committees": committee_count,
                    "hearings": hearing_count,
                },
                "connection_pool": {
                    "size": getattr(db_manager, 'pool_size', 'unknown'),
                    "checked_out": getattr(db_manager, 'checked_out_connections', 'unknown'),
                }
            }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "response_time_ms": (time.time() - start_time) * 1000,
        }


@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "congressional_data_api",
        "version": settings.api_version,
        "environment": settings.environment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/healthz", response_model=Dict[str, Any])
async def detailed_health_check():
    """Detailed health check endpoint with dependency checks."""
    start_time = time.time()
    
    # Check database
    db_health = check_database_health()
    
    # Overall status
    overall_status = "healthy" if db_health["status"] == "healthy" else "unhealthy"
    
    response = {
        "status": overall_status,
        "service": "congressional_data_api",
        "version": settings.api_version,
        "environment": settings.environment,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "response_time_ms": round((time.time() - start_time) * 1000, 2),
        "checks": {
            "database": db_health,
        },
        "configuration": {
            "debug": settings.debug,
            "log_level": settings.log_level,
            "cors_origins": len(settings.cors_origins),
            "rate_limiting": {
                "requests_per_minute": settings.rate_limit_requests,
                "burst_allowance": settings.rate_limit_burst,
            }
        }
    }
    
    return response


@router.get("/metrics", response_model=Dict[str, Any])
async def metrics():
    """Performance metrics endpoint."""
    if not settings.metrics_enabled:
        return {"error": "Metrics disabled"}
    
    start_time = time.time()
    
    # Get system metrics
    system_metrics = get_system_metrics()
    
    # Get database metrics
    db_metrics = check_database_health()
    
    response = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "response_time_ms": round((time.time() - start_time) * 1000, 2),
        "system": system_metrics,
        "database": db_metrics,
        "application": {
            "environment": settings.environment,
            "version": settings.api_version,
            "uptime_seconds": time.time() - psutil.Process().create_time(),
        }
    }
    
    return response


@router.get("/status", response_model=Dict[str, Any])
async def service_status():
    """Service status overview."""
    return {
        "service": "congressional_data_api",
        "status": "operational",
        "version": settings.api_version,
        "environment": settings.environment,
        "features": {
            "rate_limiting": settings.is_production or settings.is_staging,
            "security_headers": settings.security_headers_enabled,
            "metrics": settings.metrics_enabled,
            "caching": settings.cache_enabled,
        },
        "endpoints": {
            "health": "/health",
            "detailed_health": "/healthz",
            "metrics": "/metrics",
            "documentation": "/docs" if not settings.is_production else None,
        },
        "limits": {
            "max_page_size": settings.max_page_size,
            "default_page_size": settings.default_page_size,
            "rate_limit_requests": settings.rate_limit_requests,
            "rate_limit_period": settings.rate_limit_period,
        }
    }


@router.get("/ping")
async def ping():
    """Simple ping endpoint for load balancer health checks."""
    return {"ping": "pong", "timestamp": datetime.now(timezone.utc).isoformat()}