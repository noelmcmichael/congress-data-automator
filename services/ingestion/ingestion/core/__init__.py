"""
Core configuration and utilities for the ingestion service.

This module provides:
- Configuration management
- Database connection handling
- Logging setup
- Common utilities
"""

from .config import settings
from .database import get_db, engine
from .logging import setup_logging

__all__ = ["settings", "get_db", "engine", "setup_logging"]