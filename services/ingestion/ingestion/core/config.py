"""
Configuration settings for the congressional data ingestion service.

This module provides configuration management using Pydantic settings
with environment variable support as per rules.md standards.
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
import structlog

logger = structlog.get_logger()


class IngestionSettings(BaseSettings):
    """
    Configuration settings for the ingestion service.
    
    All settings can be overridden via environment variables.
    Critical settings like API keys are required.
    """
    
    # Application metadata
    app_name: str = "Congressional Data Ingestion Service"
    app_version: str = "0.1.0"
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database configuration
    database_url: str = Field(..., env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    max_pool_size: int = Field(default=20, env="DB_MAX_POOL_SIZE")
    pool_timeout: int = Field(default=30, env="DB_POOL_TIMEOUT")
    
    # Congress.gov API configuration
    congress_api_key: str = Field(..., env="CONGRESS_API_KEY")
    congress_api_base_url: str = "https://api.congress.gov/v3"
    congress_api_rate_limit: int = 5000  # requests per day
    congress_api_request_delay: float = 1.0  # seconds between requests
    congress_api_timeout: int = 30  # request timeout in seconds
    
    # Web scraping configuration
    scraping_delay: float = 1.0  # seconds between requests
    scraping_timeout: int = 30  # seconds
    scraping_max_retries: int = 3
    scraping_user_agent: str = (
        "Congressional Data Automator "
        "(https://github.com/noelmcmichael/congress-data-automator)"
    )
    
    # Logging configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")  # json or text
    
    # Google Cloud Platform
    gcp_project_id: Optional[str] = Field(default=None, env="GCP_PROJECT_ID")
    gcp_location: str = Field(default="us-central1", env="GCP_LOCATION")
    
    # Dagster configuration
    dagster_home: str = Field(default="/tmp/dagster", env="DAGSTER_HOME")
    
    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    
    # Service discovery
    validation_service_url: Optional[str] = Field(
        default=None, env="VALIDATION_SERVICE_URL"
    )
    api_service_url: Optional[str] = Field(
        default=None, env="API_SERVICE_URL"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    def __post_init__(self) -> None:
        """Post-initialization validation and logging setup."""
        logger.info(
            "Ingestion service configuration loaded",
            environment=self.environment,
            debug=self.debug,
            congress_api_configured=bool(self.congress_api_key),
            database_configured=bool(self.database_url),
        )


# Global settings instance
settings = IngestionSettings()


def validate_configuration() -> bool:
    """
    Validate that all required configuration is present and valid.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    
    Raises:
        ValueError: If critical configuration is missing or invalid
    """
    errors = []
    
    # Validate required environment variables
    if not settings.congress_api_key:
        errors.append("CONGRESS_API_KEY is required")
    
    if not settings.database_url:
        errors.append("DATABASE_URL is required")
    
    if not settings.secret_key:
        errors.append("SECRET_KEY is required")
    
    # Validate API key format (should be 32+ characters)
    if len(settings.congress_api_key) < 32:
        errors.append("CONGRESS_API_KEY appears to be invalid (too short)")
    
    # Validate database URL format
    if not settings.database_url.startswith(("postgresql://", "postgres://")):
        errors.append("DATABASE_URL must be a PostgreSQL connection string")
    
    if errors:
        error_msg = "Configuration validation failed: " + "; ".join(errors)
        logger.error("Configuration validation failed", errors=errors)
        raise ValueError(error_msg)
    
    logger.info("Configuration validation passed")
    return True