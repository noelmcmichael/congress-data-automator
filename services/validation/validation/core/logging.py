"""Structured logging configuration for the validation service."""

import logging
import sys
from typing import Any, Dict, Optional

import structlog
from structlog.typing import FilteringBoundLogger

from .config import settings


def setup_logging() -> FilteringBoundLogger:
    """
    Set up structured logging for the validation service.
    
    Returns:
        FilteringBoundLogger: Configured logger instance
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level),
    )

    # Configure structlog
    structlog.configure(
        processors=[
            # Add service context to all log records
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            add_service_context,
            # JSON formatting for production, colored output for development
            structlog.processors.JSONRenderer()
            if settings.is_production
            else structlog.dev.ConsoleRenderer(colors=True),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.log_level)
        ),
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Create and return logger
    logger = structlog.get_logger()
    logger.info(
        "Logging configured",
        service_name=settings.service_name,
        service_version=settings.service_version,
        environment=settings.service_environment,
        log_level=settings.log_level,
    )
    
    return logger


def add_service_context(
    logger: logging.Logger, method_name: str, event_dict: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add service context to all log records.
    
    Args:
        logger: The logger instance
        method_name: The logging method name
        event_dict: The event dictionary
        
    Returns:
        Dict[str, Any]: Updated event dictionary with service context
    """
    event_dict["service_name"] = settings.service_name
    event_dict["service_version"] = settings.service_version
    event_dict["environment"] = settings.service_environment
    
    return event_dict


def get_logger(name: Optional[str] = None) -> FilteringBoundLogger:
    """
    Get a logger instance with optional name context.
    
    Args:
        name: Optional logger name for context
        
    Returns:
        FilteringBoundLogger: Logger instance
    """
    logger = structlog.get_logger()
    if name:
        logger = logger.bind(component=name)
    return logger


def log_pipeline_start(
    logger: FilteringBoundLogger,
    pipeline_name: str,
    run_id: str,
    **kwargs: Any,
) -> None:
    """
    Log pipeline start event.
    
    Args:
        logger: Logger instance
        pipeline_name: Name of the pipeline
        run_id: Unique run identifier
        **kwargs: Additional context
    """
    logger.info(
        "Pipeline started",
        pipeline_name=pipeline_name,
        run_id=run_id,
        event_type="pipeline_start",
        **kwargs,
    )


def log_pipeline_success(
    logger: FilteringBoundLogger,
    pipeline_name: str,
    run_id: str,
    duration_seconds: float,
    records_processed: int,
    **kwargs: Any,
) -> None:
    """
    Log pipeline success event.
    
    Args:
        logger: Logger instance
        pipeline_name: Name of the pipeline
        run_id: Unique run identifier
        duration_seconds: Pipeline execution duration
        records_processed: Number of records processed
        **kwargs: Additional context
    """
    logger.info(
        "Pipeline completed successfully",
        pipeline_name=pipeline_name,
        run_id=run_id,
        duration_seconds=duration_seconds,
        records_processed=records_processed,
        event_type="pipeline_success",
        **kwargs,
    )


def log_pipeline_failure(
    logger: FilteringBoundLogger,
    pipeline_name: str,
    run_id: str,
    duration_seconds: float,
    error: str,
    **kwargs: Any,
) -> None:
    """
    Log pipeline failure event.
    
    Args:
        logger: Logger instance
        pipeline_name: Name of the pipeline
        run_id: Unique run identifier
        duration_seconds: Pipeline execution duration before failure
        error: Error message
        **kwargs: Additional context
    """
    logger.error(
        "Pipeline failed",
        pipeline_name=pipeline_name,
        run_id=run_id,
        duration_seconds=duration_seconds,
        error=error,
        event_type="pipeline_failure",
        **kwargs,
    )


def log_validation_result(
    logger: FilteringBoundLogger,
    table_name: str,
    expectation_suite: str,
    success: bool,
    result_count: int,
    **kwargs: Any,
) -> None:
    """
    Log data validation result.
    
    Args:
        logger: Logger instance
        table_name: Name of the table being validated
        expectation_suite: Name of the expectation suite
        success: Whether validation succeeded
        result_count: Number of validation results
        **kwargs: Additional context
    """
    logger.info(
        "Data validation completed",
        table_name=table_name,
        expectation_suite=expectation_suite,
        success=success,
        result_count=result_count,
        event_type="validation_result",
        **kwargs,
    )


def log_data_promotion(
    logger: FilteringBoundLogger,
    table_name: str,
    source_schema: str,
    target_schema: str,
    records_promoted: int,
    **kwargs: Any,
) -> None:
    """
    Log data promotion event.
    
    Args:
        logger: Logger instance
        table_name: Name of the table being promoted
        source_schema: Source schema name
        target_schema: Target schema name
        records_promoted: Number of records promoted
        **kwargs: Additional context
    """
    logger.info(
        "Data promotion completed",
        table_name=table_name,
        source_schema=source_schema,
        target_schema=target_schema,
        records_promoted=records_promoted,
        event_type="data_promotion",
        **kwargs,
    )