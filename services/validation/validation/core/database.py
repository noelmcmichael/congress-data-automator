"""Database connection and management for the validation service."""

import time
from contextlib import contextmanager
from typing import Dict, Generator, Optional, Any

import sqlalchemy as sa
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from .config import settings
from .logging import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Database connection manager for the validation service."""

    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            database_url: Database connection URL (defaults to settings)
        """
        self.database_url = database_url or settings.database_url
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self.logger = logger.bind(component="database_manager")

    @property
    def engine(self) -> Engine:
        """Get database engine, creating it if necessary."""
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine

    @property
    def session_factory(self) -> sessionmaker:
        """Get session factory, creating it if necessary."""
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
            )
        return self._session_factory

    def _create_engine(self) -> Engine:
        """Create database engine with connection pooling."""
        self.logger.info("Creating database engine")
        
        engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            pool_pre_ping=True,
            pool_recycle=3600,  # Recycle connections after 1 hour
            echo=settings.log_level == "DEBUG",
        )
        
        self.logger.info(
            "Database engine created",
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
        )
        
        return engine

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get database session with automatic cleanup.
        
        Yields:
            Session: Database session
        """
        session = self.session_factory()
        try:
            yield session
        except Exception as e:
            self.logger.error("Database session error", error=str(e))
            session.rollback()
            raise
        finally:
            session.close()

    def health_check(self) -> Dict[str, Any]:
        """
        Perform database health check.
        
        Returns:
            Dict[str, Any]: Health check results
        """
        start_time = time.time()
        
        try:
            with self.get_session() as session:
                # Test basic connectivity
                session.execute(text("SELECT 1"))
                
                # Check if staging schema exists
                staging_exists = session.execute(
                    text("""
                        SELECT EXISTS (
                            SELECT 1 FROM information_schema.schemata 
                            WHERE schema_name = :schema_name
                        )
                    """),
                    {"schema_name": settings.staging_schema}
                ).scalar()
                
                # Check if production schema exists
                production_exists = session.execute(
                    text("""
                        SELECT EXISTS (
                            SELECT 1 FROM information_schema.schemata 
                            WHERE schema_name = :schema_name
                        )
                    """),
                    {"schema_name": settings.production_schema}
                ).scalar()
                
                # Get connection pool stats
                pool = self.engine.pool
                
                response_time = time.time() - start_time
                
                return {
                    "healthy": True,
                    "response_time_seconds": response_time,
                    "schemas": {
                        "staging_exists": staging_exists,
                        "production_exists": production_exists,
                    },
                    "connection_pool": {
                        "size": pool.size(),
                        "checked_in": pool.checkedin(),
                        "checked_out": pool.checkedout(),
                        "overflow": pool.overflow(),
                    },
                }
                
        except Exception as e:
            response_time = time.time() - start_time
            self.logger.error("Database health check failed", error=str(e))
            
            return {
                "healthy": False,
                "response_time_seconds": response_time,
                "error": str(e),
            }

    def get_staging_table_info(self) -> Dict[str, Any]:
        """
        Get information about staging tables.
        
        Returns:
            Dict[str, Any]: Staging table information
        """
        with self.get_session() as session:
            # Get list of staging tables
            staging_tables = session.execute(
                text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = :schema_name
                    ORDER BY table_name
                """),
                {"schema_name": settings.staging_schema}
            ).fetchall()
            
            table_info = {}
            
            for (table_name,) in staging_tables:
                # Get row count
                row_count = session.execute(
                    text(f"SELECT COUNT(*) FROM {settings.staging_schema}.{table_name}")
                ).scalar()
                
                # Get last updated timestamp if available
                try:
                    last_updated = session.execute(
                        text(f"""
                            SELECT MAX(updated_at) 
                            FROM {settings.staging_schema}.{table_name}
                        """)
                    ).scalar()
                except Exception:
                    last_updated = None
                
                table_info[table_name] = {
                    "row_count": row_count,
                    "last_updated": last_updated.isoformat() if last_updated else None,
                }
            
            return table_info

    def get_production_table_info(self) -> Dict[str, Any]:
        """
        Get information about production tables.
        
        Returns:
            Dict[str, Any]: Production table information
        """
        with self.get_session() as session:
            # Get list of production tables with version suffix
            production_tables = session.execute(
                text("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = :schema_name
                    AND table_name LIKE '%_v%'
                    ORDER BY table_name
                """),
                {"schema_name": settings.production_schema}
            ).fetchall()
            
            table_info = {}
            
            for (table_name,) in production_tables:
                # Get row count
                row_count = session.execute(
                    text(f"SELECT COUNT(*) FROM {settings.production_schema}.{table_name}")
                ).scalar()
                
                # Get last updated timestamp if available
                try:
                    last_updated = session.execute(
                        text(f"""
                            SELECT MAX(updated_at) 
                            FROM {settings.production_schema}.{table_name}
                        """)
                    ).scalar()
                except Exception:
                    last_updated = None
                
                table_info[table_name] = {
                    "row_count": row_count,
                    "last_updated": last_updated.isoformat() if last_updated else None,
                }
            
            return table_info

    def create_schemas(self) -> None:
        """Create required schemas if they don't exist."""
        with self.get_session() as session:
            # Create staging schema
            session.execute(
                text(f"CREATE SCHEMA IF NOT EXISTS {settings.staging_schema}")
            )
            
            # Create production schema (usually 'public' which exists by default)
            if settings.production_schema != "public":
                session.execute(
                    text(f"CREATE SCHEMA IF NOT EXISTS {settings.production_schema}")
                )
            
            session.commit()
            
            self.logger.info(
                "Database schemas created",
                staging_schema=settings.staging_schema,
                production_schema=settings.production_schema,
            )

    def close(self) -> None:
        """Close database connections."""
        if self._engine:
            self._engine.dispose()
            self.logger.info("Database connections closed")


# Global database manager instance
db_manager = DatabaseManager()