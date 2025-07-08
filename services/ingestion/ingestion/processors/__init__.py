"""
Data processors for transforming and staging congressional data.

This module contains processors that handle:
- Data transformation and normalization
- Staging table writes
- Data deduplication and validation
- ETL pipeline coordination
"""

from .data_processor import DataProcessor

__all__ = ["DataProcessor"]