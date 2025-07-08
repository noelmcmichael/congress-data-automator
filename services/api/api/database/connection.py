"""Database connection and session management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from ..core.config import settings
from ..core.logging import logger
from .models import Base


class DatabaseManager:
    """Database connection and session manager."""
    
    def __init__(self):
        self.engine = None
        self.async_engine = None
        self.session_factory = None
        self.async_session_factory = None
        self._initialized = False
    
    def initialize(self):
        """Initialize database connections."""
        if self._initialized:
            return
        
        try:
            # Create synchronous engine
            self.engine = create_engine(
                settings.database_url,
                pool_size=settings.database_pool_size,
                max_overflow=settings.database_max_overflow,
                pool_timeout=settings.database_pool_timeout,
                pool_pre_ping=True,
                echo=settings.debug,
            )
            
            # Create session factory
            self.session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
            )
            
            # Create async engine for async operations (if not using sqlite)
            if not settings.database_url.startswith("sqlite"):
                async_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
                self.async_engine = create_async_engine(
                    async_url,
                    pool_size=settings.database_pool_size,
                    max_overflow=settings.database_max_overflow,
                    pool_timeout=settings.database_pool_timeout,
                    pool_pre_ping=True,
                    echo=settings.debug,
                )
            else:
                # For SQLite, we'll skip async for now
                self.async_engine = None
            
            # Create async session factory
            if self.async_engine:
                self.async_session_factory = async_sessionmaker(
                    bind=self.async_engine,
                    class_=AsyncSession,
                    autocommit=False,
                    autoflush=False,
                )
            else:
                self.async_session_factory = None
            
            self._initialized = True
            logger.info("Database manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database manager: {e}")
            raise
    
    def create_tables(self):
        """Create database tables."""
        if not self._initialized:
            self.initialize()
        
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a database session."""
        if not self._initialized:
            self.initialize()
        
        return self.session_factory()
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get an async database session."""
        if not self._initialized:
            self.initialize()
        
        if not self.async_session_factory:
            raise NotImplementedError("Async sessions not available for this database type")
        
        async with self.async_session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    def health_check(self) -> dict:
        """Perform database health check."""
        if not self._initialized:
            return {
                "status": "unhealthy",
                "error": "Database not initialized",
                "connected": False,
                "latency_ms": None,
            }
        
        try:
            import time
            start_time = time.time()
            
            with self.get_session() as session:
                # Simple query to test connection
                result = session.execute(text("SELECT 1"))
                result.fetchone()
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "status": "healthy",
                "connected": True,
                "latency_ms": latency_ms,
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "connected": False,
                "latency_ms": None,
            }
    
    def close(self):
        """Close database connections."""
        if self.engine:
            self.engine.dispose()
        if self.async_engine:
            self.async_engine.dispose()
        
        self._initialized = False
        logger.info("Database connections closed")


# Global database manager instance
db_manager = DatabaseManager()


def get_db() -> Session:
    """Dependency for getting database session."""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session."""
    async with db_manager.get_async_session() as session:
        yield session