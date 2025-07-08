"""
Congressional Data Validation Service

Enterprise-grade data validation and quality assurance for Congressional data.
Transforms raw staging data into validated production data using Great Expectations
and Dagster orchestration.
"""

__version__ = "0.1.0"
__author__ = "Congressional Data Team"

from .core.config import Settings
from .core.database import DatabaseManager
from .core.logging import setup_logging

__all__ = ["Settings", "DatabaseManager", "setup_logging"]