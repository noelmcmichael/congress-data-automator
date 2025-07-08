"""Dagster assets for validation pipeline."""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List

from dagster import asset, AssetIn, AssetKey, MetadataValue, Output
from sqlalchemy import text

from ..core.config import settings
from ..core.logging import get_logger, log_validation_result, log_data_promotion
from ..models.congressional import ValidationResult, DataPromotion
from ..expectations.suites import get_expectation_suite
from .resources import database_resource, expectation_resource

logger = get_logger(__name__)


# Staging Assets (read from staging schema)
@asset(
    name="staging_members",
    description="Members data from staging schema",
    group_name="staging",
    compute_kind="sql",
)
def staging_members(context, database: database_resource) -> pd.DataFrame:
    """Load members data from staging schema."""
    query = f"SELECT * FROM {settings.staging_schema}.members"
    
    with database.get_session() as session:
        result = session.execute(text(query))
        data = result.fetchall()
        columns = result.keys()
        
        df = pd.DataFrame(data, columns=columns)
        
        context.log.info(f"Loaded {len(df)} members from staging schema")
        context.add_output_metadata({
            "num_rows": len(df),
            "columns": list(df.columns),
            "schema": settings.staging_schema,
            "table": "members",
        })
        
        return df


@asset(
    name="staging_committees",
    description="Committees data from staging schema",
    group_name="staging",
    compute_kind="sql",
)
def staging_committees(context, database: database_resource) -> pd.DataFrame:
    """Load committees data from staging schema."""
    query = f"SELECT * FROM {settings.staging_schema}.committees"
    
    with database.get_session() as session:
        result = session.execute(text(query))
        data = result.fetchall()
        columns = result.keys()
        
        df = pd.DataFrame(data, columns=columns)
        
        context.log.info(f"Loaded {len(df)} committees from staging schema")
        context.add_output_metadata({
            "num_rows": len(df),
            "columns": list(df.columns),
            "schema": settings.staging_schema,
            "table": "committees",
        })
        
        return df


@asset(
    name="staging_hearings",
    description="Hearings data from staging schema",
    group_name="staging",
    compute_kind="sql",
)
def staging_hearings(context, database: database_resource) -> pd.DataFrame:
    """Load hearings data from staging schema."""
    query = f"SELECT * FROM {settings.staging_schema}.hearings"
    
    with database.get_session() as session:
        result = session.execute(text(query))
        data = result.fetchall()
        columns = result.keys()
        
        df = pd.DataFrame(data, columns=columns)
        
        context.log.info(f"Loaded {len(df)} hearings from staging schema")
        context.add_output_metadata({
            "num_rows": len(df),
            "columns": list(df.columns),
            "schema": settings.staging_schema,
            "table": "hearings",
        })
        
        return df


# Validation Assets (apply Great Expectations validation)
@asset(
    name="validated_members",
    description="Members data validated with Great Expectations",
    ins={"staging_members": AssetIn("staging_members")},
    group_name="validation",
    compute_kind="great_expectations",
)
def validated_members(context, staging_members: pd.DataFrame, expectations: expectation_resource) -> Output[ValidationResult]:
    """Validate members data using Great Expectations."""
    table_name = "members"
    suite_name = f"{table_name}_suite"
    
    # Run validation
    validation_result = expectations.validate_table(
        table_name=table_name,
        suite_name=suite_name,
        schema_name=settings.staging_schema,
    )
    
    # Log validation result
    log_validation_result(
        logger,
        table_name=table_name,
        expectation_suite=suite_name,
        success=validation_result.success,
        result_count=validation_result.results_count,
    )
    
    # Add metadata to Dagster
    context.add_output_metadata({
        "validation_success": validation_result.success,
        "success_rate": validation_result.success_rate,
        "expectations_run": validation_result.results_count,
        "expectations_passed": validation_result.successful_expectations,
        "expectations_failed": validation_result.unsuccessful_expectations,
        "duration_seconds": validation_result.duration_seconds,
        "validation_details": MetadataValue.json(validation_result.validation_details),
    })
    
    # If validation fails, raise an error
    if not validation_result.success:
        raise ValueError(f"Validation failed for {table_name}: {validation_result.unsuccessful_expectations} expectations failed")
    
    return Output(
        value=validation_result,
        metadata={
            "table_name": table_name,
            "success_rate": validation_result.success_rate,
            "duration_seconds": validation_result.duration_seconds,
        }
    )


@asset(
    name="validated_committees",
    description="Committees data validated with Great Expectations",
    ins={"staging_committees": AssetIn("staging_committees")},
    group_name="validation",
    compute_kind="great_expectations",
)
def validated_committees(context, staging_committees: pd.DataFrame, expectations: expectation_resource) -> Output[ValidationResult]:
    """Validate committees data using Great Expectations."""
    table_name = "committees"
    suite_name = f"{table_name}_suite"
    
    # Run validation
    validation_result = expectations.validate_table(
        table_name=table_name,
        suite_name=suite_name,
        schema_name=settings.staging_schema,
    )
    
    # Log validation result
    log_validation_result(
        logger,
        table_name=table_name,
        expectation_suite=suite_name,
        success=validation_result.success,
        result_count=validation_result.results_count,
    )
    
    # Add metadata to Dagster
    context.add_output_metadata({
        "validation_success": validation_result.success,
        "success_rate": validation_result.success_rate,
        "expectations_run": validation_result.results_count,
        "expectations_passed": validation_result.successful_expectations,
        "expectations_failed": validation_result.unsuccessful_expectations,
        "duration_seconds": validation_result.duration_seconds,
        "validation_details": MetadataValue.json(validation_result.validation_details),
    })
    
    # If validation fails, raise an error
    if not validation_result.success:
        raise ValueError(f"Validation failed for {table_name}: {validation_result.unsuccessful_expectations} expectations failed")
    
    return Output(
        value=validation_result,
        metadata={
            "table_name": table_name,
            "success_rate": validation_result.success_rate,
            "duration_seconds": validation_result.duration_seconds,
        }
    )


@asset(
    name="validated_hearings",
    description="Hearings data validated with Great Expectations",
    ins={"staging_hearings": AssetIn("staging_hearings")},
    group_name="validation",
    compute_kind="great_expectations",
)
def validated_hearings(context, staging_hearings: pd.DataFrame, expectations: expectation_resource) -> Output[ValidationResult]:
    """Validate hearings data using Great Expectations."""
    table_name = "hearings"
    suite_name = f"{table_name}_suite"
    
    # Run validation
    validation_result = expectations.validate_table(
        table_name=table_name,
        suite_name=suite_name,
        schema_name=settings.staging_schema,
    )
    
    # Log validation result
    log_validation_result(
        logger,
        table_name=table_name,
        expectation_suite=suite_name,
        success=validation_result.success,
        result_count=validation_result.results_count,
    )
    
    # Add metadata to Dagster
    context.add_output_metadata({
        "validation_success": validation_result.success,
        "success_rate": validation_result.success_rate,
        "expectations_run": validation_result.results_count,
        "expectations_passed": validation_result.successful_expectations,
        "expectations_failed": validation_result.unsuccessful_expectations,
        "duration_seconds": validation_result.duration_seconds,
        "validation_details": MetadataValue.json(validation_result.validation_details),
    })
    
    # If validation fails, raise an error
    if not validation_result.success:
        raise ValueError(f"Validation failed for {table_name}: {validation_result.unsuccessful_expectations} expectations failed")
    
    return Output(
        value=validation_result,
        metadata={
            "table_name": table_name,
            "success_rate": validation_result.success_rate,
            "duration_seconds": validation_result.duration_seconds,
        }
    )


# Production Assets (promote validated data to production)
@asset(
    name="production_members",
    description="Members data promoted to production schema",
    ins={"validated_members": AssetIn("validated_members")},
    group_name="production",
    compute_kind="sql",
)
def production_members(context, validated_members: ValidationResult, database: database_resource) -> Output[DataPromotion]:
    """Promote validated members data to production schema."""
    table_name = "members"
    target_table = f"{table_name}{settings.versioned_table_suffix}"
    
    promotion_id = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    started_at = datetime.now()
    
    try:
        # Create versioned production table
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {settings.production_schema}.{target_table} AS
        SELECT * FROM {settings.staging_schema}.{table_name}
        WHERE 1=0
        """
        
        # Clear existing data and insert new data
        with database.get_session() as session:
            # Create table structure
            session.execute(text(create_table_query))
            
            # Clear existing data
            session.execute(text(f"DELETE FROM {settings.production_schema}.{target_table}"))
            
            # Insert validated data
            insert_query = f"""
            INSERT INTO {settings.production_schema}.{target_table}
            SELECT * FROM {settings.staging_schema}.{table_name}
            """
            
            result = session.execute(text(insert_query))
            records_promoted = result.rowcount
            
            # Create or update current view
            view_query = f"""
            CREATE OR REPLACE VIEW {settings.production_schema}.{table_name} AS
            SELECT * FROM {settings.production_schema}.{target_table}
            """
            session.execute(text(view_query))
            
            session.commit()
            
        completed_at = datetime.now()
        
        # Create promotion record
        promotion = DataPromotion(
            promotion_id=promotion_id,
            table_name=table_name,
            source_schema=settings.staging_schema,
            target_schema=settings.production_schema,
            target_table=target_table,
            records_processed=records_promoted,
            records_promoted=records_promoted,
            records_failed=0,
            success=True,
            started_at=started_at,
            completed_at=completed_at,
        )
        
        # Log promotion
        log_data_promotion(
            logger,
            table_name=table_name,
            source_schema=settings.staging_schema,
            target_schema=settings.production_schema,
            records_promoted=records_promoted,
        )
        
        context.add_output_metadata({
            "promotion_success": True,
            "records_promoted": records_promoted,
            "target_table": target_table,
            "duration_seconds": promotion.duration_seconds,
            "success_rate": promotion.success_rate,
        })
        
        return Output(
            value=promotion,
            metadata={
                "table_name": table_name,
                "records_promoted": records_promoted,
                "success_rate": promotion.success_rate,
            }
        )
        
    except Exception as e:
        completed_at = datetime.now()
        
        # Create failed promotion record
        promotion = DataPromotion(
            promotion_id=promotion_id,
            table_name=table_name,
            source_schema=settings.staging_schema,
            target_schema=settings.production_schema,
            target_table=target_table,
            records_processed=0,
            records_promoted=0,
            records_failed=0,
            success=False,
            error_message=str(e),
            started_at=started_at,
            completed_at=completed_at,
        )
        
        context.log.error(f"Failed to promote {table_name}: {str(e)}")
        raise e


@asset(
    name="production_committees",
    description="Committees data promoted to production schema",
    ins={"validated_committees": AssetIn("validated_committees")},
    group_name="production",
    compute_kind="sql",
)
def production_committees(context, validated_committees: ValidationResult, database: database_resource) -> Output[DataPromotion]:
    """Promote validated committees data to production schema."""
    table_name = "committees"
    target_table = f"{table_name}{settings.versioned_table_suffix}"
    
    promotion_id = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    started_at = datetime.now()
    
    try:
        # Create versioned production table
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {settings.production_schema}.{target_table} AS
        SELECT * FROM {settings.staging_schema}.{table_name}
        WHERE 1=0
        """
        
        # Clear existing data and insert new data
        with database.get_session() as session:
            # Create table structure
            session.execute(text(create_table_query))
            
            # Clear existing data
            session.execute(text(f"DELETE FROM {settings.production_schema}.{target_table}"))
            
            # Insert validated data
            insert_query = f"""
            INSERT INTO {settings.production_schema}.{target_table}
            SELECT * FROM {settings.staging_schema}.{table_name}
            """
            
            result = session.execute(text(insert_query))
            records_promoted = result.rowcount
            
            # Create or update current view
            view_query = f"""
            CREATE OR REPLACE VIEW {settings.production_schema}.{table_name} AS
            SELECT * FROM {settings.production_schema}.{target_table}
            """
            session.execute(text(view_query))
            
            session.commit()
            
        completed_at = datetime.now()
        
        # Create promotion record
        promotion = DataPromotion(
            promotion_id=promotion_id,
            table_name=table_name,
            source_schema=settings.staging_schema,
            target_schema=settings.production_schema,
            target_table=target_table,
            records_processed=records_promoted,
            records_promoted=records_promoted,
            records_failed=0,
            success=True,
            started_at=started_at,
            completed_at=completed_at,
        )
        
        # Log promotion
        log_data_promotion(
            logger,
            table_name=table_name,
            source_schema=settings.staging_schema,
            target_schema=settings.production_schema,
            records_promoted=records_promoted,
        )
        
        context.add_output_metadata({
            "promotion_success": True,
            "records_promoted": records_promoted,
            "target_table": target_table,
            "duration_seconds": promotion.duration_seconds,
            "success_rate": promotion.success_rate,
        })
        
        return Output(
            value=promotion,
            metadata={
                "table_name": table_name,
                "records_promoted": records_promoted,
                "success_rate": promotion.success_rate,
            }
        )
        
    except Exception as e:
        completed_at = datetime.now()
        
        # Create failed promotion record
        promotion = DataPromotion(
            promotion_id=promotion_id,
            table_name=table_name,
            source_schema=settings.staging_schema,
            target_schema=settings.production_schema,
            target_table=target_table,
            records_processed=0,
            records_promoted=0,
            records_failed=0,
            success=False,
            error_message=str(e),
            started_at=started_at,
            completed_at=completed_at,
        )
        
        context.log.error(f"Failed to promote {table_name}: {str(e)}")
        raise e


@asset(
    name="production_hearings",
    description="Hearings data promoted to production schema",
    ins={"validated_hearings": AssetIn("validated_hearings")},
    group_name="production",
    compute_kind="sql",
)
def production_hearings(context, validated_hearings: ValidationResult, database: database_resource) -> Output[DataPromotion]:
    """Promote validated hearings data to production schema."""
    table_name = "hearings"
    target_table = f"{table_name}{settings.versioned_table_suffix}"
    
    promotion_id = f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    started_at = datetime.now()
    
    try:
        # Create versioned production table
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {settings.production_schema}.{target_table} AS
        SELECT * FROM {settings.staging_schema}.{table_name}
        WHERE 1=0
        """
        
        # Clear existing data and insert new data
        with database.get_session() as session:
            # Create table structure
            session.execute(text(create_table_query))
            
            # Clear existing data
            session.execute(text(f"DELETE FROM {settings.production_schema}.{target_table}"))
            
            # Insert validated data
            insert_query = f"""
            INSERT INTO {settings.production_schema}.{target_table}
            SELECT * FROM {settings.staging_schema}.{table_name}
            """
            
            result = session.execute(text(insert_query))
            records_promoted = result.rowcount
            
            # Create or update current view
            view_query = f"""
            CREATE OR REPLACE VIEW {settings.production_schema}.{table_name} AS
            SELECT * FROM {settings.production_schema}.{target_table}
            """
            session.execute(text(view_query))
            
            session.commit()
            
        completed_at = datetime.now()
        
        # Create promotion record
        promotion = DataPromotion(
            promotion_id=promotion_id,
            table_name=table_name,
            source_schema=settings.staging_schema,
            target_schema=settings.production_schema,
            target_table=target_table,
            records_processed=records_promoted,
            records_promoted=records_promoted,
            records_failed=0,
            success=True,
            started_at=started_at,
            completed_at=completed_at,
        )
        
        # Log promotion
        log_data_promotion(
            logger,
            table_name=table_name,
            source_schema=settings.staging_schema,
            target_schema=settings.production_schema,
            records_promoted=records_promoted,
        )
        
        context.add_output_metadata({
            "promotion_success": True,
            "records_promoted": records_promoted,
            "target_table": target_table,
            "duration_seconds": promotion.duration_seconds,
            "success_rate": promotion.success_rate,
        })
        
        return Output(
            value=promotion,
            metadata={
                "table_name": table_name,
                "records_promoted": records_promoted,
                "success_rate": promotion.success_rate,
            }
        )
        
    except Exception as e:
        completed_at = datetime.now()
        
        # Create failed promotion record
        promotion = DataPromotion(
            promotion_id=promotion_id,
            table_name=table_name,
            source_schema=settings.staging_schema,
            target_schema=settings.production_schema,
            target_table=target_table,
            records_processed=0,
            records_promoted=0,
            records_failed=0,
            success=False,
            error_message=str(e),
            started_at=started_at,
            completed_at=completed_at,
        )
        
        context.log.error(f"Failed to promote {table_name}: {str(e)}")
        raise e