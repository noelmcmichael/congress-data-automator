"""Main entry point for the API service."""

import os
import sys
from pathlib import Path

# Add the api module to the path
sys.path.insert(0, str(Path(__file__).parent))

from api.core.config import settings
from api.core.logging import logger
from api.database.connection import db_manager


def initialize_service():
    """Initialize the API service."""
    logger.info("Initializing API service")
    
    # Initialize database
    db_manager.initialize()
    
    # Create tables if they don't exist (for development)
    if settings.is_development:
        db_manager.create_tables()
    
    logger.info("API service initialized successfully")


# Initialize and expose app for uvicorn
initialize_service()
from api.app import app


def initialize_service():
    """Initialize the API service."""
    logger.info("Initializing API service")
    
    # Initialize database
    db_manager.initialize()
    
    # Create tables if they don't exist (for development)
    if settings.is_development:
        db_manager.create_tables()
    
    logger.info("API service initialized successfully")


def run_api_server():
    """Run the FastAPI server."""
    import uvicorn
    from api.app import app
    
    logger.info(f"Starting API server on {settings.api_host}:{settings.api_port}")
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        workers=settings.api_workers if settings.is_production else 1,
        log_config=None,  # Use our custom logging
        reload=settings.api_reload,
    )


def run_development_server():
    """Run development server with auto-reload."""
    import uvicorn
    from api.app import app
    
    logger.info(f"Starting development server on {settings.api_host}:{settings.api_port}")
    uvicorn.run(
        "api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_config=None,  # Use our custom logging
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Congressional Data API Service")
    parser.add_argument(
        "command",
        choices=["init", "api", "dev"],
        help="Command to run",
    )
    
    args = parser.parse_args()
    
    if args.command == "init":
        initialize_service()
    elif args.command == "api":
        initialize_service()
        run_api_server()
    elif args.command == "dev":
        initialize_service()
        run_development_server()
    else:
        parser.print_help()