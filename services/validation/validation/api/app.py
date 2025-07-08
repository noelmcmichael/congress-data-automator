"""FastAPI application for validation service."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..core.config import settings
from ..core.logging import setup_logging, get_logger
from ..core.database import db_manager
from ..expectations.manager import expectation_manager
from ..models.congressional import ValidationResult

# Setup logging
logger = setup_logging()
app_logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Congressional Data Validation Service",
    description="Enterprise-grade data validation and quality assurance service",
    version=settings.service_version,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Pydantic models for API
class HealthResponse(BaseModel):
    """Health check response model."""
    healthy: bool
    timestamp: datetime
    service_name: str
    service_version: str
    environment: str
    database: Dict[str, Any]


class StatusResponse(BaseModel):
    """Service status response model."""
    service_name: str
    service_version: str
    environment: str
    uptime_seconds: float
    database: Dict[str, Any]
    staging_tables: Dict[str, Any]
    production_tables: Dict[str, Any]


class ValidationRequest(BaseModel):
    """Validation request model."""
    table_name: str
    suite_name: Optional[str] = None
    schema_name: str = "staging"


class ValidationResponse(BaseModel):
    """Validation response model."""
    success: bool
    table_name: str
    suite_name: str
    run_id: str
    results_count: int
    successful_expectations: int
    unsuccessful_expectations: int
    success_rate: float
    duration_seconds: float
    details: Dict[str, Any]


class PromotionRequest(BaseModel):
    """Promotion request model."""
    table_name: str
    source_schema: str = "staging"
    target_schema: str = "public"


class PromotionResponse(BaseModel):
    """Promotion response model."""
    success: bool
    table_name: str
    promotion_id: str
    records_promoted: int
    duration_seconds: float
    target_table: str


# Global variables for tracking
app_start_time = datetime.now()


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    app_logger.info("Starting Congressional Data Validation Service")
    
    # Initialize database manager
    try:
        db_manager.create_schemas()
        app_logger.info("Database schemas initialized")
    except Exception as e:
        app_logger.error("Failed to initialize database schemas", error=str(e))
    
    # Initialize Great Expectations
    try:
        expectation_manager.initialize_data_context()
        expectation_manager.create_datasource()
        app_logger.info("Great Expectations initialized")
    except Exception as e:
        app_logger.error("Failed to initialize Great Expectations", error=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    app_logger.info("Shutting down Congressional Data Validation Service")
    db_manager.close()


@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    db_health = db_manager.health_check()
    
    return HealthResponse(
        healthy=db_health["healthy"],
        timestamp=datetime.now(),
        service_name=settings.service_name,
        service_version=settings.service_version,
        environment=settings.service_environment,
        database=db_health,
    )


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get service status and statistics."""
    uptime = (datetime.now() - app_start_time).total_seconds()
    
    db_health = db_manager.health_check()
    staging_tables = db_manager.get_staging_table_info()
    production_tables = db_manager.get_production_table_info()
    
    return StatusResponse(
        service_name=settings.service_name,
        service_version=settings.service_version,
        environment=settings.service_environment,
        uptime_seconds=uptime,
        database=db_health,
        staging_tables=staging_tables,
        production_tables=production_tables,
    )


@app.post("/validate", response_model=ValidationResponse)
async def validate_table(
    request: ValidationRequest,
    background_tasks: BackgroundTasks,
):
    """Validate a table using Great Expectations."""
    table_name = request.table_name
    suite_name = request.suite_name or f"{table_name}_suite"
    schema_name = request.schema_name
    
    app_logger.info(
        "Validation request received",
        table_name=table_name,
        suite_name=suite_name,
        schema_name=schema_name,
    )
    
    try:
        # Run validation
        result = expectation_manager.validate_table(
            table_name=table_name,
            suite_name=suite_name,
            schema_name=schema_name,
        )
        
        # Build data docs in background
        background_tasks.add_task(expectation_manager.build_data_docs)
        
        return ValidationResponse(
            success=result.success,
            table_name=result.table_name,
            suite_name=result.expectation_suite,
            run_id=result.run_id,
            results_count=result.results_count,
            successful_expectations=result.successful_expectations,
            unsuccessful_expectations=result.unsuccessful_expectations,
            success_rate=result.success_rate,
            duration_seconds=result.duration_seconds,
            details=result.validation_details,
        )
        
    except Exception as e:
        app_logger.error(
            "Validation failed",
            table_name=table_name,
            suite_name=suite_name,
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate/{table_name}", response_model=ValidationResponse)
async def validate_table_by_name(
    table_name: str,
    background_tasks: BackgroundTasks,
    suite_name: Optional[str] = None,
    schema_name: str = "staging",
):
    """Validate a specific table by name."""
    request = ValidationRequest(
        table_name=table_name,
        suite_name=suite_name,
        schema_name=schema_name,
    )
    return await validate_table(request, background_tasks)


@app.post("/promote", response_model=PromotionResponse)
async def promote_table(request: PromotionRequest):
    """Promote validated data to production schema."""
    table_name = request.table_name
    source_schema = request.source_schema
    target_schema = request.target_schema
    
    app_logger.info(
        "Promotion request received",
        table_name=table_name,
        source_schema=source_schema,
        target_schema=target_schema,
    )
    
    try:
        # This is a simplified promotion - in practice, you'd use the Dagster pipeline
        from ..models.congressional import DataPromotion
        from sqlalchemy import text
        
        promotion_id = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        started_at = datetime.now()
        
        target_table = f"{table_name}{settings.versioned_table_suffix}"
        
        with db_manager.get_session() as session:
            # Create versioned production table
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {target_schema}.{target_table} AS
            SELECT * FROM {source_schema}.{table_name}
            WHERE 1=0
            """
            session.execute(text(create_table_query))
            
            # Clear existing data
            session.execute(text(f"DELETE FROM {target_schema}.{target_table}"))
            
            # Insert validated data
            insert_query = f"""
            INSERT INTO {target_schema}.{target_table}
            SELECT * FROM {source_schema}.{table_name}
            """
            result = session.execute(text(insert_query))
            records_promoted = result.rowcount
            
            # Create or update current view
            view_query = f"""
            CREATE OR REPLACE VIEW {target_schema}.{table_name} AS
            SELECT * FROM {target_schema}.{target_table}
            """
            session.execute(text(view_query))
            
            session.commit()
            
        completed_at = datetime.now()
        duration = (completed_at - started_at).total_seconds()
        
        app_logger.info(
            "Promotion completed",
            table_name=table_name,
            promotion_id=promotion_id,
            records_promoted=records_promoted,
            duration_seconds=duration,
        )
        
        return PromotionResponse(
            success=True,
            table_name=table_name,
            promotion_id=promotion_id,
            records_promoted=records_promoted,
            duration_seconds=duration,
            target_table=target_table,
        )
        
    except Exception as e:
        app_logger.error(
            "Promotion failed",
            table_name=table_name,
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/promote/{table_name}", response_model=PromotionResponse)
async def promote_table_by_name(
    table_name: str,
    source_schema: str = "staging",
    target_schema: str = "public",
):
    """Promote a specific table by name."""
    request = PromotionRequest(
        table_name=table_name,
        source_schema=source_schema,
        target_schema=target_schema,
    )
    return await promote_table(request)


@app.get("/validation-results", response_model=List[Dict[str, Any]])
async def get_validation_results(limit: int = 10):
    """Get recent validation results."""
    try:
        results = expectation_manager.get_validation_results(limit=limit)
        return results
    except Exception as e:
        app_logger.error("Failed to get validation results", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data-docs")
async def get_data_docs():
    """Get link to Great Expectations data documentation."""
    try:
        # Build data docs
        expectation_manager.build_data_docs()
        
        # Return path to data docs
        docs_path = f"{settings.ge_data_context_root}/data_docs/local_site/index.html"
        
        return {
            "data_docs_url": f"file://{docs_path}",
            "message": "Data documentation built successfully",
        }
    except Exception as e:
        app_logger.error("Failed to build data docs", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
async def get_metrics():
    """Get Prometheus-style metrics."""
    try:
        # Basic metrics
        uptime = (datetime.now() - app_start_time).total_seconds()
        
        # Database metrics
        db_health = db_manager.health_check()
        staging_tables = db_manager.get_staging_table_info()
        production_tables = db_manager.get_production_table_info()
        
        metrics = {
            "validation_service_uptime_seconds": uptime,
            "validation_service_healthy": 1 if db_health["healthy"] else 0,
            "validation_service_database_response_time_seconds": db_health.get("response_time_seconds", 0),
        }
        
        # Table metrics
        for table_name, info in staging_tables.items():
            metrics[f"staging_table_row_count{{table=\"{table_name}\"}}"] = info.get("row_count", 0)
            
        for table_name, info in production_tables.items():
            metrics[f"production_table_row_count{{table=\"{table_name}\"}}"] = info.get("row_count", 0)
        
        # Format as Prometheus metrics
        prometheus_metrics = []
        for metric_name, value in metrics.items():
            prometheus_metrics.append(f"{metric_name} {value}")
        
        return JSONResponse(
            content="\n".join(prometheus_metrics),
            media_type="text/plain",
        )
        
    except Exception as e:
        app_logger.error("Failed to get metrics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)