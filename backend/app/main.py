"""
Main FastAPI application for Congressional Data Automation Service.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
from .core.config import settings
from .core.database import engine, Base
from .core.database_optimization import setup_database_optimization
from .services.congress_api import CongressApiClient
from .middleware.cache_middleware import CacheMiddleware, warm_cache
from .middleware.security_middleware import (
    RateLimitMiddleware, 
    SecurityHeadersMiddleware, 
    RequestValidationMiddleware,
    security_monitor
)

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

# Add security middleware (order matters - security first)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestValidationMiddleware, max_request_size=1024*1024)  # 1MB limit
app.add_middleware(RateLimitMiddleware, calls=100, period=60)  # 100 req/min

# Add caching middleware (after security)
app.add_middleware(CacheMiddleware, cache_enabled=True)

# Import models to ensure they're registered with Base
from .models import Member, Committee, CommitteeMembership, Hearing, Witness, HearingDocument, CongressionalSession

# Create database tables (commented out for deployment - tables already exist)
# Base.metadata.create_all(bind=engine)

# Initialize API client
congress_api = CongressApiClient()


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting Congressional Data Automation Service")
    
    # Setup database optimization
    try:
        optimization_results = await setup_database_optimization()
        logger.info(f"Database optimization complete: {optimization_results}")
    except Exception as e:
        logger.warning(f"Database optimization failed: {e}")
    
    # Warm up cache
    try:
        cache_endpoints = await warm_cache()
        logger.info(f"Cache warm-up complete for {cache_endpoints} endpoints")
    except Exception as e:
        logger.warning(f"Cache warm-up failed: {e}")


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
    from .core.cache import cache_manager
    from .core.database_optimization import db_optimizer
    
    rate_limit_status = congress_api.get_rate_limit_status()
    
    # Get cache status
    cache_status = "enabled" if cache_manager.redis_client else "memory_only"
    
    # Get performance stats
    try:
        perf_stats = await db_optimizer.analyze_query_performance()
    except:
        perf_stats = {"error": "unavailable"}
    
    return {
        "api_status": "active",
        "congress_api_rate_limit": rate_limit_status,
        "database_status": "connected",
        "cache_status": cache_status,
        "performance_optimization": "enabled",
        "database_stats": perf_stats,
        "version": settings.app_version,
    }


@app.get("/api/v1/cache/status")
async def cache_status():
    """Cache status and statistics endpoint."""
    from .core.cache import cache_manager
    
    try:
        cache_info = {
            "redis_available": cache_manager.redis_client is not None,
            "memory_cache_entries": len(cache_manager.memory_cache),
            "cache_type": "redis" if cache_manager.redis_client else "memory",
        }
        
        if cache_manager.redis_client:
            try:
                redis_info = cache_manager.redis_client.info()
                cache_info["redis_memory_usage"] = redis_info.get("used_memory_human", "N/A")
                cache_info["redis_connected_clients"] = redis_info.get("connected_clients", "N/A")
            except:
                cache_info["redis_status"] = "connection_error"
        
        return cache_info
    except Exception as e:
        return {"error": str(e), "cache_status": "unavailable"}


@app.post("/api/v1/cache/invalidate/{data_type}")
async def invalidate_cache(data_type: str):
    """Manually invalidate cache for specific data type."""
    from .middleware.cache_middleware import cache_invalidator
    
    try:
        invalidated_count = await cache_invalidator.invalidate_cache(data_type)
        return {
            "data_type": data_type,
            "invalidated_entries": invalidated_count,
            "status": "success"
        }
    except Exception as e:
        return {
            "data_type": data_type,
            "error": str(e),
            "status": "failed"
        }


@app.get("/api/v1/security/status")
async def security_status():
    """Security status and monitoring endpoint."""
    from .core.security import get_security_status
    
    try:
        status = get_security_status()
        return status
    except Exception as e:
        return {"error": str(e), "security_status": "unavailable"}


@app.get("/api/v1/security/events")
async def security_events():
    """Get recent security events summary."""
    try:
        events_summary = security_monitor.get_security_summary()
        return {
            "security_events": events_summary,
            "monitoring_status": "active",
            "timestamp": "2025-01-08T23:00:00Z"
        }
    except Exception as e:
        return {"error": str(e), "events": "unavailable"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Include API routers
from .api.v1 import data_updates, data_retrieval, relationships, congressional_sessions, advanced_features, monitoring_dashboard
app.include_router(data_updates.router, prefix=settings.api_v1_prefix, tags=["data-updates"])
app.include_router(data_retrieval.router, prefix=settings.api_v1_prefix, tags=["data-retrieval"])
app.include_router(relationships.router, prefix=settings.api_v1_prefix, tags=["relationships"])
app.include_router(congressional_sessions.router, prefix=settings.api_v1_prefix + "/congress", tags=["congressional-sessions"])
app.include_router(advanced_features.router, prefix=settings.api_v1_prefix, tags=["advanced-features"])
app.include_router(monitoring_dashboard.router, prefix=settings.api_v1_prefix, tags=["monitoring"])


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