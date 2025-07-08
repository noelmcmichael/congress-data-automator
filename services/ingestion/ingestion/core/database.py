"""
Database connection and session management for the ingestion service.

This module provides database connectivity with proper connection pooling,
transaction management, and error handling as per rules.md standards.
"""

from typing import Generator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import structlog

from .config import settings

logger = structlog.get_logger()

# Create database engine with connection pooling
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    poolclass=QueuePool,
    pool_size=settings.max_pool_size,
    max_overflow=0,
    pool_timeout=settings.pool_timeout,
    pool_pre_ping=True,  # Validate connections before use
    connect_args={
        "connect_timeout": 10,
        "application_name": "congressional-ingestion"
    }
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for staging models
Base = declarative_base()

# Metadata for staging tables (separate from production schema)
staging_metadata = MetaData(schema="staging")


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.
    
    Yields:
        Session: SQLAlchemy session with proper cleanup
        
    This function provides:
    - Automatic session cleanup
    - Transaction rollback on exceptions
    - Connection pool management
    - Logging of database operations
    """
    db = SessionLocal()
    try:
        logger.debug("Database session created")
        yield db
    except Exception as e:
        logger.error(
            "Database session error",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=e
        )
        db.rollback()
        raise
    finally:
        db.close()
        logger.debug("Database session closed")


def create_staging_tables() -> None:
    """
    Create staging tables for the ingestion service.
    
    This function creates the staging schema and tables
    used for raw data ingestion before validation.
    """
    try:
        # Create staging schema if it doesn't exist
        with engine.connect() as conn:
            conn.execute("CREATE SCHEMA IF NOT EXISTS staging")
            conn.commit()
        
        # Create staging tables
        staging_metadata.create_all(bind=engine)
        
        logger.info(
            "Staging tables created successfully",
            schema="staging"
        )
    except Exception as e:
        logger.error(
            "Failed to create staging tables",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=e
        )
        raise


def health_check() -> bool:
    """
    Check database connectivity and health.
    
    Returns:
        bool: True if database is healthy, False otherwise
        
    This function:
    - Tests basic connectivity
    - Validates schema access
    - Checks connection pool status
    """
    try:
        with engine.connect() as conn:
            # Test basic connectivity
            result = conn.execute("SELECT 1")
            result.fetchone()
            
            # Check staging schema exists
            result = conn.execute(
                "SELECT schema_name FROM information_schema.schemata "
                "WHERE schema_name = 'staging'"
            )
            staging_exists = result.fetchone() is not None
            
        # Check connection pool status
        pool_status = {
            "size": engine.pool.size(),
            "checked_in": engine.pool.checkedin(),
            "checked_out": engine.pool.checkedout(),
            "overflow": engine.pool.overflow(),
        }
        
        logger.debug(
            "Database health check passed",
            staging_schema_exists=staging_exists,
            pool_status=pool_status
        )
        
        return True
        
    except Exception as e:
        logger.error(
            "Database health check failed",
            error_type=type(e).__name__,
            error_message=str(e),
            exc_info=e
        )
        return False


class DatabaseManager:
    """
    Database manager for handling staging operations.
    
    This class provides higher-level database operations
    specifically for the ingestion service needs.
    """
    
    def __init__(self):
        self.logger = structlog.get_logger(self.__class__.__name__)
    
    def bulk_insert(
        self, 
        session: Session, 
        model_class: type, 
        data: list, 
        batch_size: int = 1000
    ) -> int:
        """
        Perform bulk insert operation with batching.
        
        Args:
            session: Database session
            model_class: SQLAlchemy model class
            data: List of dictionaries to insert
            batch_size: Number of records per batch
            
        Returns:
            int: Number of records inserted
        """
        total_inserted = 0
        
        try:
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                
                # Create model instances
                instances = [model_class(**item) for item in batch]
                
                # Bulk insert
                session.bulk_save_objects(instances)
                session.commit()
                
                total_inserted += len(batch)
                
                self.logger.debug(
                    "Batch inserted",
                    model=model_class.__name__,
                    batch_size=len(batch),
                    total_inserted=total_inserted,
                    progress=f"{i + len(batch)}/{len(data)}"
                )
            
            self.logger.info(
                "Bulk insert completed",
                model=model_class.__name__,
                total_records=total_inserted
            )
            
            return total_inserted
            
        except Exception as e:
            session.rollback()
            self.logger.error(
                "Bulk insert failed",
                model=model_class.__name__,
                error_type=type(e).__name__,
                error_message=str(e),
                exc_info=e
            )
            raise
    
    def truncate_staging_table(self, session: Session, table_name: str) -> None:
        """
        Truncate a staging table for fresh data load.
        
        Args:
            session: Database session
            table_name: Name of the staging table
        """
        try:
            session.execute(f"TRUNCATE TABLE staging.{table_name} CASCADE")
            session.commit()
            
            self.logger.info(
                "Staging table truncated",
                table=f"staging.{table_name}"
            )
            
        except Exception as e:
            session.rollback()
            self.logger.error(
                "Failed to truncate staging table",
                table=f"staging.{table_name}",
                error_type=type(e).__name__,
                error_message=str(e),
                exc_info=e
            )
            raise