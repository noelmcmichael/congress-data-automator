"""CLI utilities for the validation service."""

import typer
from typing import Optional
from pathlib import Path

from .core.config import settings
from .core.logging import setup_logging
from .core.database import db_manager
from .expectations.manager import expectation_manager
from .expectations.suites import create_all_expectation_suites

app = typer.Typer(
    name="validation",
    help="Congressional Data Validation Service CLI",
    add_completion=False,
)

# Setup logging
logger = setup_logging()


@app.command()
def init():
    """Initialize the validation service."""
    typer.echo("Initializing Congressional Data Validation Service...")
    
    # Create database schemas
    typer.echo("Creating database schemas...")
    db_manager.create_schemas()
    typer.echo("✓ Database schemas created")
    
    # Initialize Great Expectations
    typer.echo("Initializing Great Expectations...")
    expectation_manager.initialize_data_context()
    expectation_manager.create_datasource()
    typer.echo("✓ Great Expectations initialized")
    
    # Create expectation suites
    typer.echo("Creating expectation suites...")
    create_all_expectation_suites(expectation_manager)
    typer.echo("✓ Expectation suites created")
    
    # Build data docs
    typer.echo("Building data documentation...")
    expectation_manager.build_data_docs()
    typer.echo("✓ Data documentation built")
    
    typer.echo("🎉 Validation service initialized successfully!")


@app.command()
def validate(
    table: str = typer.Argument(..., help="Table name to validate"),
    suite: Optional[str] = typer.Option(None, help="Expectation suite name"),
    schema: str = typer.Option("staging", help="Database schema name"),
):
    """Validate a table using Great Expectations."""
    suite_name = suite or f"{table}_suite"
    
    typer.echo(f"Validating table: {schema}.{table}")
    typer.echo(f"Using expectation suite: {suite_name}")
    
    try:
        result = expectation_manager.validate_table(
            table_name=table,
            suite_name=suite_name,
            schema_name=schema,
        )
        
        if result.success:
            typer.echo(f"✓ Validation successful!")
            typer.echo(f"  Success rate: {result.success_rate:.1f}%")
            typer.echo(f"  Expectations run: {result.results_count}")
            typer.echo(f"  Duration: {result.duration_seconds:.2f}s")
        else:
            typer.echo(f"✗ Validation failed!")
            typer.echo(f"  Success rate: {result.success_rate:.1f}%")
            typer.echo(f"  Failed expectations: {result.unsuccessful_expectations}")
            typer.echo(f"  Duration: {result.duration_seconds:.2f}s")
            raise typer.Exit(1)
            
    except Exception as e:
        typer.echo(f"✗ Validation error: {e}")
        raise typer.Exit(1)


@app.command()
def promote(
    table: str = typer.Argument(..., help="Table name to promote"),
    source: str = typer.Option("staging", help="Source schema name"),
    target: str = typer.Option("public", help="Target schema name"),
):
    """Promote validated data to production schema."""
    typer.echo(f"Promoting table: {source}.{table} → {target}.{table}")
    
    try:
        from .models.congressional import DataPromotion
        from datetime import datetime
        from sqlalchemy import text
        
        promotion_id = f"{table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        started_at = datetime.now()
        
        target_table = f"{table}{settings.versioned_table_suffix}"
        
        with db_manager.get_session() as session:
            # Create versioned production table
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {target}.{target_table} AS
            SELECT * FROM {source}.{table}
            WHERE 1=0
            """
            session.execute(text(create_table_query))
            
            # Clear existing data
            session.execute(text(f"DELETE FROM {target}.{target_table}"))
            
            # Insert validated data
            insert_query = f"""
            INSERT INTO {target}.{target_table}
            SELECT * FROM {source}.{table}
            """
            result = session.execute(text(insert_query))
            records_promoted = result.rowcount
            
            # Create or update current view
            view_query = f"""
            CREATE OR REPLACE VIEW {target}.{table} AS
            SELECT * FROM {target}.{target_table}
            """
            session.execute(text(view_query))
            
            session.commit()
            
        completed_at = datetime.now()
        duration = (completed_at - started_at).total_seconds()
        
        typer.echo(f"✓ Promotion successful!")
        typer.echo(f"  Records promoted: {records_promoted}")
        typer.echo(f"  Target table: {target_table}")
        typer.echo(f"  Duration: {duration:.2f}s")
        
    except Exception as e:
        typer.echo(f"✗ Promotion error: {e}")
        raise typer.Exit(1)


@app.command()
def status():
    """Show service status."""
    typer.echo("Congressional Data Validation Service Status")
    typer.echo("=" * 45)
    
    # Service info
    typer.echo(f"Service: {settings.service_name}")
    typer.echo(f"Version: {settings.service_version}")
    typer.echo(f"Environment: {settings.service_environment}")
    typer.echo()
    
    # Database health
    db_health = db_manager.health_check()
    if db_health["healthy"]:
        typer.echo(f"✓ Database: Healthy ({db_health['response_time_seconds']:.3f}s)")
    else:
        typer.echo(f"✗ Database: Unhealthy - {db_health.get('error', 'Unknown error')}")
    
    # Schema info
    if db_health["healthy"] and "schemas" in db_health:
        schemas = db_health["schemas"]
        staging_status = "✓" if schemas["staging_exists"] else "✗"
        production_status = "✓" if schemas["production_exists"] else "✗"
        typer.echo(f"{staging_status} Staging schema: {settings.staging_schema}")
        typer.echo(f"{production_status} Production schema: {settings.production_schema}")
    
    # Table info
    try:
        staging_tables = db_manager.get_staging_table_info()
        typer.echo(f"\nStaging Tables ({len(staging_tables)}):")
        for table_name, info in staging_tables.items():
            last_updated = info["last_updated"] or "Never"
            typer.echo(f"  {table_name}: {info['row_count']} rows (updated: {last_updated})")
            
        production_tables = db_manager.get_production_table_info()
        typer.echo(f"\nProduction Tables ({len(production_tables)}):")
        for table_name, info in production_tables.items():
            last_updated = info["last_updated"] or "Never"
            typer.echo(f"  {table_name}: {info['row_count']} rows (updated: {last_updated})")
            
    except Exception as e:
        typer.echo(f"✗ Could not get table info: {e}")


@app.command()
def docs():
    """Build and show data documentation."""
    typer.echo("Building Great Expectations data documentation...")
    
    try:
        expectation_manager.build_data_docs()
        docs_path = Path(settings.ge_data_context_root) / "data_docs" / "local_site" / "index.html"
        
        if docs_path.exists():
            typer.echo(f"✓ Data documentation built successfully!")
            typer.echo(f"  Open: file://{docs_path.absolute()}")
        else:
            typer.echo(f"✗ Data documentation not found at expected location")
            
    except Exception as e:
        typer.echo(f"✗ Failed to build data documentation: {e}")
        raise typer.Exit(1)


@app.command()
def test():
    """Run validation tests on all tables."""
    typer.echo("Running validation tests...")
    
    tables = ["members", "committees", "hearings"]
    results = {}
    
    for table in tables:
        typer.echo(f"\nTesting {table}...")
        
        try:
            result = expectation_manager.validate_table(
                table_name=table,
                suite_name=f"{table}_suite",
                schema_name="staging",
            )
            
            results[table] = result
            
            if result.success:
                typer.echo(f"  ✓ {table}: PASSED ({result.success_rate:.1f}%)")
            else:
                typer.echo(f"  ✗ {table}: FAILED ({result.success_rate:.1f}%)")
                
        except Exception as e:
            typer.echo(f"  ✗ {table}: ERROR - {e}")
            results[table] = None
    
    # Summary
    typer.echo(f"\nValidation Test Summary:")
    typer.echo("=" * 25)
    
    passed = sum(1 for r in results.values() if r and r.success)
    failed = sum(1 for r in results.values() if r and not r.success)
    errors = sum(1 for r in results.values() if r is None)
    
    typer.echo(f"Passed: {passed}")
    typer.echo(f"Failed: {failed}")
    typer.echo(f"Errors: {errors}")
    
    if failed > 0 or errors > 0:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()