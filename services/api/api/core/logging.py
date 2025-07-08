"""Logging configuration for the API service."""

import logging
import sys
from typing import Any, Dict, Optional

import structlog
from structlog.types import Processor

from .config import settings


def setup_logging() -> structlog.stdlib.BoundLogger:
    """Set up structured logging."""
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level),
    )

    # Configure structlog
    processors: list[Processor] = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # Add context processors
    processors.extend([
        add_service_context,
        add_request_context,
    ])

    # Add appropriate renderer based on environment
    if settings.is_production:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Return logger
    return structlog.get_logger("congressional_data_api")


def add_service_context(logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add service context to log events."""
    event_dict.update({
        "service": "congressional_data_api",
        "version": "0.1.0",
        "environment": settings.environment,
    })
    return event_dict


def add_request_context(logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Add request context to log events."""
    # This will be enhanced when we add FastAPI request context
    return event_dict


class LoggingMiddleware:
    """Middleware for logging HTTP requests."""
    
    def __init__(self, logger: Optional[structlog.stdlib.BoundLogger] = None):
        self.logger = logger or structlog.get_logger("congressional_data_api")
    
    async def __call__(self, request, call_next):
        """Process request and log details."""
        # Log request
        start_time = structlog.get_logger().info(
            "Request started",
            method=request.method,
            path=request.url.path,
            query_params=str(request.query_params),
            client_ip=request.client.host if request.client else "unknown",
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Log response
            self.logger.info(
                "Request completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                client_ip=request.client.host if request.client else "unknown",
            )
            
            return response
            
        except Exception as e:
            # Log error
            self.logger.error(
                "Request failed",
                method=request.method,
                path=request.url.path,
                error=str(e),
                client_ip=request.client.host if request.client else "unknown",
            )
            raise


# Global logger instance
logger = setup_logging()