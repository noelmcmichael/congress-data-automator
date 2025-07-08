"""
Structured logging configuration for the ingestion service.

This module configures structured logging using structlog as per rules.md
standards for enterprise-grade observability.
"""

import logging
import sys
from typing import Any, Dict, Optional
import structlog
from structlog.typing import FilteringBoundLogger

from .config import settings


def setup_logging() -> FilteringBoundLogger:
    """
    Configure structured logging for the ingestion service.
    
    Returns:
        FilteringBoundLogger: Configured logger instance
    
    This function sets up:
    - JSON or text output based on configuration
    - Appropriate log levels
    - Request ID correlation
    - Performance metrics
    - Error tracking
    """
    
    # Configure Python's standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )
    
    # Suppress noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    # Configure structlog processors based on format preference
    if settings.log_format.lower() == "json":
        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            add_correlation_id,
            add_service_context,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ]
    else:
        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            add_correlation_id,
            add_service_context,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    logger = structlog.get_logger("ingestion")
    logger.info(
        "Logging configured",
        service="congressional-ingestion",
        version=settings.app_version,
        environment=settings.environment,
        log_level=settings.log_level,
        log_format=settings.log_format,
    )
    
    return logger


def add_correlation_id(
    logger: logging.Logger, 
    name: str, 
    event_dict: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add correlation ID to log entries for request tracing.
    
    Args:
        logger: Logger instance
        name: Logger name
        event_dict: Event dictionary to modify
        
    Returns:
        Dict[str, Any]: Modified event dictionary with correlation ID
    """
    # Try to get correlation ID from context (would be set by middleware)
    correlation_id = getattr(logger, "_correlation_id", None)
    if correlation_id:
        event_dict["correlation_id"] = correlation_id
    
    return event_dict


def add_service_context(
    logger: logging.Logger, 
    name: str, 
    event_dict: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add service context information to log entries.
    
    Args:
        logger: Logger instance
        name: Logger name
        event_dict: Event dictionary to modify
        
    Returns:
        Dict[str, Any]: Modified event dictionary with service context
    """
    event_dict.update({
        "service": "congressional-ingestion",
        "version": settings.app_version,
        "environment": settings.environment,
    })
    
    return event_dict


def get_logger(name: Optional[str] = None) -> FilteringBoundLogger:
    """
    Get a configured logger instance.
    
    Args:
        name: Optional logger name for categorization
        
    Returns:
        FilteringBoundLogger: Configured logger instance
    """
    if name:
        return structlog.get_logger(name)
    return structlog.get_logger()


class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    
    This provides a consistent way to add structured logging
    to collectors, processors, and other service components.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = get_logger(self.__class__.__name__)
    
    def log_operation_start(self, operation: str, **context) -> None:
        """Log the start of an operation with context."""
        self.logger.info(
            f"{operation} started",
            operation=operation,
            **context
        )
    
    def log_operation_success(
        self, 
        operation: str, 
        duration_ms: Optional[float] = None,
        **context
    ) -> None:
        """Log successful completion of an operation."""
        log_data = {
            "operation": operation,
            **context
        }
        if duration_ms is not None:
            log_data["duration_ms"] = duration_ms
            
        self.logger.info(
            f"{operation} completed successfully",
            **log_data
        )
    
    def log_operation_error(
        self, 
        operation: str, 
        error: Exception,
        duration_ms: Optional[float] = None,
        **context
    ) -> None:
        """Log operation failure with error details."""
        log_data = {
            "operation": operation,
            "error_type": type(error).__name__,
            "error_message": str(error),
            **context
        }
        if duration_ms is not None:
            log_data["duration_ms"] = duration_ms
            
        self.logger.error(
            f"{operation} failed",
            **log_data,
            exc_info=error
        )