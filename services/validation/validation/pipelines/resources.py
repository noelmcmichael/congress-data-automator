"""Dagster resources for validation pipeline."""

import time
from typing import Dict, Any
from contextlib import contextmanager

from dagster import resource, ConfigurableResource, InitResourceContext
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from ..core.config import settings
from ..core.database import db_manager
from ..core.logging import get_logger
from ..expectations.manager import expectation_manager

logger = get_logger(__name__)


class DatabaseResource(ConfigurableResource):
    """Database resource for Dagster pipeline."""
    
    database_url: str = settings.database_url
    
    def get_session(self):
        """Get database session."""
        return db_manager.get_session()
    
    def get_engine(self):
        """Get database engine."""
        return db_manager.engine
    
    def health_check(self) -> Dict[str, Any]:
        """Perform database health check."""
        return db_manager.health_check()
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        """Execute a database query."""
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            session.commit()
            return result


class ExpectationResource(ConfigurableResource):
    """Great Expectations resource for Dagster pipeline."""
    
    data_context_root: str = settings.ge_data_context_root
    
    def get_manager(self):
        """Get expectation manager."""
        return expectation_manager
    
    def validate_table(self, table_name: str, suite_name: str, schema_name: str = "staging"):
        """Validate a table using Great Expectations."""
        return expectation_manager.validate_table(
            table_name=table_name,
            suite_name=suite_name,
            schema_name=schema_name,
        )
    
    def initialize_context(self):
        """Initialize Great Expectations context."""
        return expectation_manager.initialize_data_context()
    
    def create_datasource(self, datasource_name: str = "postgresql_datasource"):
        """Create PostgreSQL datasource."""
        return expectation_manager.create_datasource(datasource_name)


# Legacy resource functions for backward compatibility
@resource(
    config_schema={
        "database_url": {"default": settings.database_url},
        "pool_size": {"default": settings.database_pool_size},
        "max_overflow": {"default": settings.database_max_overflow},
    }
)
def database_resource(init_context: InitResourceContext):
    """Database resource for Dagster pipeline."""
    config = init_context.resource_config
    
    engine = create_engine(
        config["database_url"],
        poolclass=QueuePool,
        pool_size=config["pool_size"],
        max_overflow=config["max_overflow"],
        pool_pre_ping=True,
        pool_recycle=3600,
    )
    
    session_factory = sessionmaker(bind=engine)
    
    @contextmanager
    def get_session():
        session = session_factory()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    class DatabaseConnection:
        def __init__(self):
            self.engine = engine
            self.session_factory = session_factory
            
        def get_session(self):
            return get_session()
            
        def execute_query(self, query: str, params: Dict[str, Any] = None):
            with get_session() as session:
                result = session.execute(text(query), params or {})
                session.commit()
                return result
                
        def health_check(self) -> Dict[str, Any]:
            start_time = time.time()
            try:
                with get_session() as session:
                    session.execute(text("SELECT 1"))
                    response_time = time.time() - start_time
                    return {
                        "healthy": True,
                        "response_time_seconds": response_time,
                    }
            except Exception as e:
                response_time = time.time() - start_time
                return {
                    "healthy": False,
                    "response_time_seconds": response_time,
                    "error": str(e),
                }
    
    try:
        yield DatabaseConnection()
    finally:
        engine.dispose()


@resource(
    config_schema={
        "data_context_root": {"default": settings.ge_data_context_root},
    }
)
def expectation_resource(init_context: InitResourceContext):
    """Great Expectations resource for Dagster pipeline."""
    config = init_context.resource_config
    
    from ..expectations.manager import ExpectationManager
    
    manager = ExpectationManager(config["data_context_root"])
    
    class ExpectationConnection:
        def __init__(self):
            self.manager = manager
            
        def validate_table(self, table_name: str, suite_name: str, schema_name: str = "staging"):
            return self.manager.validate_table(
                table_name=table_name,
                suite_name=suite_name,
                schema_name=schema_name,
            )
            
        def initialize_context(self):
            return self.manager.initialize_data_context()
            
        def create_datasource(self, datasource_name: str = "postgresql_datasource"):
            return self.manager.create_datasource(datasource_name)
    
    yield ExpectationConnection()


# Resource instances for modern Dagster
database_resource_instance = DatabaseResource()
expectation_resource_instance = ExpectationResource()