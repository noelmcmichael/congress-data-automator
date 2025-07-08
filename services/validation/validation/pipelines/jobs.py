"""Dagster jobs for validation pipeline."""

from dagster import (
    define_asset_job,
    AssetSelection,
    SkipReason,
    job,
    op,
    RunRequest,
    sensor,
    DefaultSensorStatus,
    DagsterRunStatus,
    RunsFilter,
    schedule,
    ScheduleEvaluationContext,
)
from datetime import datetime, timedelta
from typing import List, Optional

from ..core.config import settings
from ..core.logging import get_logger, log_pipeline_start, log_pipeline_success, log_pipeline_failure

logger = get_logger(__name__)


# Asset Selection Patterns
staging_assets = AssetSelection.groups("staging")
validation_assets = AssetSelection.groups("validation")
production_assets = AssetSelection.groups("production")

# Full pipeline selection
full_pipeline_assets = staging_assets | validation_assets | production_assets


# Jobs
validation_job = define_asset_job(
    name="validation_job",
    description="Validate staging data using Great Expectations",
    selection=staging_assets | validation_assets,
    config={
        "execution": {
            "config": {
                "multiprocess": {
                    "max_concurrent": 3,
                }
            }
        }
    },
)

promotion_job = define_asset_job(
    name="promotion_job", 
    description="Promote validated data to production schema",
    selection=validation_assets | production_assets,
    config={
        "execution": {
            "config": {
                "multiprocess": {
                    "max_concurrent": 3,
                }
            }
        }
    },
)

full_pipeline_job = define_asset_job(
    name="full_pipeline_job",
    description="Run complete validation and promotion pipeline",
    selection=full_pipeline_assets,
    config={
        "execution": {
            "config": {
                "multiprocess": {
                    "max_concurrent": 3,
                }
            }
        }
    },
)

# Individual table jobs
members_pipeline_job = define_asset_job(
    name="members_pipeline_job",
    description="Run validation and promotion for members table only",
    selection=AssetSelection.assets([
        "staging_members",
        "validated_members", 
        "production_members",
    ]),
)

committees_pipeline_job = define_asset_job(
    name="committees_pipeline_job",
    description="Run validation and promotion for committees table only",
    selection=AssetSelection.assets([
        "staging_committees",
        "validated_committees",
        "production_committees", 
    ]),
)

hearings_pipeline_job = define_asset_job(
    name="hearings_pipeline_job",
    description="Run validation and promotion for hearings table only",
    selection=AssetSelection.assets([
        "staging_hearings",
        "validated_hearings",
        "production_hearings",
    ]),
)


# Operational Jobs
@op
def check_data_freshness(context) -> dict:
    """Check data freshness in staging tables."""
    from ..core.database import db_manager
    from sqlalchemy import text
    
    freshness_info = {}
    tables = ["members", "committees", "hearings"]
    
    with db_manager.get_session() as session:
        for table in tables:
            try:
                # Check if table exists
                table_exists = session.execute(text(f"""
                    SELECT EXISTS (
                        SELECT 1 FROM information_schema.tables 
                        WHERE table_schema = '{settings.staging_schema}' 
                        AND table_name = '{table}'
                    )
                """)).scalar()
                
                if not table_exists:
                    freshness_info[table] = {
                        "exists": False,
                        "error": "Table does not exist",
                    }
                    continue
                
                # Get row count
                row_count = session.execute(text(f"""
                    SELECT COUNT(*) FROM {settings.staging_schema}.{table}
                """)).scalar()
                
                # Get last update time if available
                try:
                    last_updated = session.execute(text(f"""
                        SELECT MAX(updated_at) FROM {settings.staging_schema}.{table}
                    """)).scalar()
                except Exception:
                    last_updated = None
                
                freshness_info[table] = {
                    "exists": True,
                    "row_count": row_count,
                    "last_updated": last_updated.isoformat() if last_updated else None,
                    "is_fresh": (
                        last_updated is not None and 
                        last_updated > datetime.now() - timedelta(hours=24)
                    ) if last_updated else False,
                }
                
            except Exception as e:
                freshness_info[table] = {
                    "exists": False,
                    "error": str(e),
                }
    
    context.log.info(f"Data freshness check completed: {freshness_info}")
    return freshness_info


@job(
    name="data_freshness_check",
    description="Check data freshness in staging tables",
)
def data_freshness_check_job():
    """Job to check data freshness."""
    return check_data_freshness()


@op
def cleanup_old_versions(context) -> dict:
    """Clean up old versioned tables."""
    from ..core.database import db_manager
    from sqlalchemy import text
    
    cleanup_info = {}
    tables = ["members", "committees", "hearings"]
    
    with db_manager.get_session() as session:
        for table in tables:
            try:
                # Find all versioned tables for this base table
                versioned_tables = session.execute(text(f"""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = '{settings.production_schema}' 
                    AND table_name LIKE '{table}_v%'
                    ORDER BY table_name
                """)).fetchall()
                
                table_names = [row[0] for row in versioned_tables]
                
                # Keep only the latest N versions (default: 3)
                versions_to_keep = 3
                if len(table_names) > versions_to_keep:
                    tables_to_drop = table_names[:-versions_to_keep]
                    
                    for table_to_drop in tables_to_drop:
                        session.execute(text(f"DROP TABLE IF EXISTS {settings.production_schema}.{table_to_drop}"))
                        context.log.info(f"Dropped old table: {table_to_drop}")
                    
                    session.commit()
                    
                    cleanup_info[table] = {
                        "total_versions": len(table_names),
                        "versions_kept": versions_to_keep,
                        "versions_dropped": len(tables_to_drop),
                        "dropped_tables": tables_to_drop,
                    }
                else:
                    cleanup_info[table] = {
                        "total_versions": len(table_names),
                        "versions_kept": len(table_names),
                        "versions_dropped": 0,
                        "dropped_tables": [],
                    }
                    
            except Exception as e:
                cleanup_info[table] = {
                    "error": str(e),
                }
    
    context.log.info(f"Version cleanup completed: {cleanup_info}")
    return cleanup_info


@job(
    name="version_cleanup",
    description="Clean up old versioned tables",
)
def version_cleanup_job():
    """Job to clean up old versions."""
    return cleanup_old_versions()


# Sensors
@sensor(
    name="staging_data_sensor",
    description="Sensor to trigger validation when staging data is updated",
    job=validation_job,
    default_status=DefaultSensorStatus.STOPPED,
)
def staging_data_sensor(context):
    """Sensor to detect when staging data is updated."""
    freshness_info = {}
    
    # Check data freshness
    from ..core.database import db_manager
    from sqlalchemy import text
    
    with db_manager.get_session() as session:
        tables = ["members", "committees", "hearings"]
        
        for table in tables:
            try:
                # Check if table has been updated recently
                last_updated = session.execute(text(f"""
                    SELECT MAX(updated_at) FROM {settings.staging_schema}.{table}
                """)).scalar()
                
                if last_updated:
                    freshness_info[table] = {
                        "last_updated": last_updated,
                        "is_fresh": last_updated > datetime.now() - timedelta(hours=1),
                    }
                    
            except Exception as e:
                context.log.warning(f"Could not check freshness for {table}: {e}")
    
    # Check if we should trigger a run
    fresh_tables = [
        table for table, info in freshness_info.items() 
        if info.get("is_fresh", False)
    ]
    
    if fresh_tables:
        context.log.info(f"Fresh data detected in tables: {fresh_tables}")
        yield RunRequest(
            run_key=f"staging_data_sensor_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            tags={
                "sensor": "staging_data_sensor",
                "fresh_tables": ",".join(fresh_tables),
            },
        )
    else:
        context.log.info("No fresh data detected")


@sensor(
    name="validation_success_sensor",
    description="Sensor to trigger promotion when validation succeeds",
    job=promotion_job,
    default_status=DefaultSensorStatus.STOPPED,
)
def validation_success_sensor(context):
    """Sensor to detect when validation succeeds and trigger promotion."""
    # Check for recent successful validation runs
    recent_runs = context.instance.get_runs(
        filters=RunsFilter(
            job_names=["validation_job"],
            created_after=datetime.now() - timedelta(hours=1),
            statuses=[DagsterRunStatus.SUCCESS],
        )
    )
    
    if recent_runs:
        latest_run = recent_runs[0]
        
        # Check if promotion has already been triggered for this validation
        promotion_runs = context.instance.get_runs(
            filters=RunsFilter(
                job_names=["promotion_job"],
                created_after=latest_run.created_timestamp,
                tags={"validation_run_id": latest_run.run_id},
            )
        )
        
        if not promotion_runs:
            context.log.info(f"Triggering promotion for validation run: {latest_run.run_id}")
            yield RunRequest(
                run_key=f"promotion_{latest_run.run_id}",
                tags={
                    "sensor": "validation_success_sensor",
                    "validation_run_id": latest_run.run_id,
                },
            )
        else:
            context.log.info("Promotion already triggered for latest validation run")
    else:
        context.log.info("No recent successful validation runs found")


# Schedule configurations

@schedule(
    name="daily_validation_schedule",
    description="Run validation pipeline daily at 6 AM",
    job=validation_job,
    cron_schedule="0 6 * * *",  # 6 AM daily
)
def daily_validation_schedule(context: ScheduleEvaluationContext):
    """Daily validation schedule."""
    return RunRequest(
        run_key=f"daily_validation_{datetime.now().strftime('%Y%m%d')}",
        tags={
            "schedule": "daily_validation_schedule",
            "run_type": "scheduled",
        },
    )


@schedule(
    name="hourly_freshness_check_schedule",
    description="Check data freshness every hour",
    job=data_freshness_check_job,
    cron_schedule="0 * * * *",  # Every hour
)
def hourly_freshness_check_schedule(context: ScheduleEvaluationContext):
    """Hourly freshness check schedule."""
    return RunRequest(
        run_key=f"freshness_check_{datetime.now().strftime('%Y%m%d_%H')}",
        tags={
            "schedule": "hourly_freshness_check_schedule",
            "run_type": "scheduled",
        },
    )


@schedule(
    name="weekly_cleanup_schedule",
    description="Clean up old versions weekly on Sunday at 2 AM",
    job=version_cleanup_job,
    cron_schedule="0 2 * * 0",  # 2 AM on Sunday
)
def weekly_cleanup_schedule(context: ScheduleEvaluationContext):
    """Weekly cleanup schedule."""
    return RunRequest(
        run_key=f"version_cleanup_{datetime.now().strftime('%Y%m%d')}",
        tags={
            "schedule": "weekly_cleanup_schedule",
            "run_type": "scheduled",
        },
    )


# Export all jobs and schedules
all_jobs = [
    validation_job,
    promotion_job,
    full_pipeline_job,
    members_pipeline_job,
    committees_pipeline_job,
    hearings_pipeline_job,
    data_freshness_check_job,
    version_cleanup_job,
]

all_schedules = [
    daily_validation_schedule,
    hourly_freshness_check_schedule,
    weekly_cleanup_schedule,
]

all_sensors = [
    staging_data_sensor,
    validation_success_sensor,
]