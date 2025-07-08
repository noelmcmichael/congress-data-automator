"""Main entry point for the validation service."""

import os
import sys
from pathlib import Path

# Add the validation module to the path
sys.path.insert(0, str(Path(__file__).parent))

from validation.core.config import settings
from validation.core.logging import setup_logging
from validation.core.database import db_manager
from validation.expectations.manager import expectation_manager
from validation.expectations.suites import create_all_expectation_suites

# Setup logging
logger = setup_logging()


def initialize_service():
    """Initialize the validation service."""
    logger.info("Initializing validation service")
    
    # Create database schemas
    db_manager.create_schemas()
    
    # Initialize Great Expectations
    expectation_manager.initialize_data_context()
    expectation_manager.create_datasource()
    
    # Create expectation suites
    create_all_expectation_suites(expectation_manager)
    
    # Build data docs
    expectation_manager.build_data_docs()
    
    logger.info("Validation service initialized successfully")


def run_dagster_webserver():
    """Run the Dagster webserver."""
    import subprocess
    
    # Set environment variables
    os.environ["DAGSTER_HOME"] = settings.dagster_home
    
    # Create dagster home directory
    Path(settings.dagster_home).mkdir(parents=True, exist_ok=True)
    
    # Run dagster webserver
    cmd = [
        "dagster",
        "dev",
        "-f",
        "validation/pipelines/definitions.py",
        "--host",
        "0.0.0.0",
        "--port",
        "3000",
    ]
    
    logger.info("Starting Dagster webserver on port 3000")
    subprocess.run(cmd)


def run_fastapi_server():
    """Run the FastAPI server."""
    import uvicorn
    from validation.api.app import app
    
    logger.info(f"Starting FastAPI server on {settings.api_host}:{settings.api_port}")
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers,
        log_config=None,  # Use our custom logging
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Congressional Data Validation Service")
    parser.add_argument(
        "command",
        choices=["init", "dagster", "api", "dev"],
        help="Command to run",
    )
    
    args = parser.parse_args()
    
    if args.command == "init":
        initialize_service()
    elif args.command == "dagster":
        initialize_service()
        run_dagster_webserver()
    elif args.command == "api":
        initialize_service()
        run_fastapi_server()
    elif args.command == "dev":
        # Development mode - run both dagster and api
        initialize_service()
        
        import threading
        import time
        
        # Start Dagster in a separate thread
        dagster_thread = threading.Thread(target=run_dagster_webserver, daemon=True)
        dagster_thread.start()
        
        # Wait a bit for Dagster to start
        time.sleep(3)
        
        # Start FastAPI server
        run_fastapi_server()
    else:
        parser.print_help()