"""
Monitoring and metrics module for Congressional API service.
"""

import time
from functools import wraps
from typing import Callable, Dict, Any
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
import structlog

logger = structlog.get_logger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active database connections'
)

CONGRESSIONAL_MEMBERS_TOTAL = Gauge(
    'congressional_members_total',
    'Total number of congressional members'
)

CONGRESSIONAL_COMMITTEES_TOTAL = Gauge(
    'congressional_committees_total',
    'Total number of congressional committees'
)

CONGRESSIONAL_HEARINGS_TOTAL = Gauge(
    'congressional_hearings_total',
    'Total number of congressional hearings'
)

CONGRESSIONAL_DATA_LAST_UPDATE = Gauge(
    'congressional_data_last_update_timestamp',
    'Timestamp of last congressional data update'
)

DATABASE_OPERATIONS = Counter(
    'database_operations_total',
    'Total database operations',
    ['operation', 'table', 'status']
)

CACHE_OPERATIONS = Counter(
    'cache_operations_total',
    'Total cache operations',
    ['operation', 'status']
)

EXTERNAL_API_CALLS = Counter(
    'external_api_calls_total',
    'Total external API calls',
    ['service', 'endpoint', 'status']
)

BACKGROUND_TASKS = Counter(
    'background_tasks_total',
    'Total background tasks',
    ['task_type', 'status']
)

class MetricsMiddleware:
    """Middleware to collect HTTP request metrics."""
    
    def __init__(self, app):
        self.app = app
        
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
            
        method = scope["method"]
        path = scope["path"]
        
        # Skip metrics collection for metrics endpoint
        if path == "/metrics":
            await self.app(scope, receive, send)
            return
            
        start_time = time.time()
        
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
                duration = time.time() - start_time
                
                # Record metrics
                REQUEST_COUNT.labels(
                    method=method,
                    endpoint=path,
                    status=status_code
                ).inc()
                
                REQUEST_DURATION.labels(
                    method=method,
                    endpoint=path
                ).observe(duration)
                
                logger.info(
                    "HTTP request completed",
                    method=method,
                    path=path,
                    status_code=status_code,
                    duration=duration
                )
                
            await send(message)
            
        await self.app(scope, receive, send_wrapper)

def track_database_operation(operation: str, table: str):
    """Decorator to track database operations."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                DATABASE_OPERATIONS.labels(
                    operation=operation,
                    table=table,
                    status="success"
                ).inc()
                return result
            except Exception as e:
                DATABASE_OPERATIONS.labels(
                    operation=operation,
                    table=table,
                    status="error"
                ).inc()
                logger.error(
                    "Database operation failed",
                    operation=operation,
                    table=table,
                    error=str(e)
                )
                raise
            finally:
                duration = time.time() - start_time
                logger.debug(
                    "Database operation completed",
                    operation=operation,
                    table=table,
                    duration=duration
                )
        return wrapper
    return decorator

def track_cache_operation(operation: str):
    """Decorator to track cache operations."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                CACHE_OPERATIONS.labels(
                    operation=operation,
                    status="success"
                ).inc()
                return result
            except Exception as e:
                CACHE_OPERATIONS.labels(
                    operation=operation,
                    status="error"
                ).inc()
                logger.error(
                    "Cache operation failed",
                    operation=operation,
                    error=str(e)
                )
                raise
        return wrapper
    return decorator

def track_external_api_call(service: str, endpoint: str):
    """Decorator to track external API calls."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                EXTERNAL_API_CALLS.labels(
                    service=service,
                    endpoint=endpoint,
                    status="success"
                ).inc()
                return result
            except Exception as e:
                EXTERNAL_API_CALLS.labels(
                    service=service,
                    endpoint=endpoint,
                    status="error"
                ).inc()
                logger.error(
                    "External API call failed",
                    service=service,
                    endpoint=endpoint,
                    error=str(e)
                )
                raise
        return wrapper
    return decorator

def track_background_task(task_type: str):
    """Decorator to track background tasks."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                BACKGROUND_TASKS.labels(
                    task_type=task_type,
                    status="success"
                ).inc()
                return result
            except Exception as e:
                BACKGROUND_TASKS.labels(
                    task_type=task_type,
                    status="error"
                ).inc()
                logger.error(
                    "Background task failed",
                    task_type=task_type,
                    error=str(e)
                )
                raise
        return wrapper
    return decorator

async def update_congressional_data_metrics(db_session):
    """Update congressional data metrics from database."""
    try:
        # Count members
        members_count = await db_session.execute(
            "SELECT COUNT(*) FROM members WHERE is_current = true"
        )
        CONGRESSIONAL_MEMBERS_TOTAL.set(members_count.scalar())
        
        # Count committees
        committees_count = await db_session.execute(
            "SELECT COUNT(*) FROM committees WHERE is_active = true"
        )
        CONGRESSIONAL_COMMITTEES_TOTAL.set(committees_count.scalar())
        
        # Count hearings
        hearings_count = await db_session.execute(
            "SELECT COUNT(*) FROM hearings"
        )
        CONGRESSIONAL_HEARINGS_TOTAL.set(hearings_count.scalar())
        
        # Update last update timestamp
        CONGRESSIONAL_DATA_LAST_UPDATE.set(time.time())
        
        logger.info(
            "Congressional data metrics updated",
            members_count=members_count.scalar(),
            committees_count=committees_count.scalar(),
            hearings_count=hearings_count.scalar()
        )
        
    except Exception as e:
        logger.error("Failed to update congressional data metrics", error=str(e))

def get_metrics():
    """Get Prometheus metrics in the correct format."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )