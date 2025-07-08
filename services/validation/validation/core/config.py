"""Configuration management for the validation service."""

from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration settings for the validation service."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database Configuration
    database_url: str = Field(
        default="postgresql://test:test@localhost:5432/test_db",
        description="PostgreSQL database connection URL",
        env="DATABASE_URL",
    )
    database_pool_size: int = Field(
        default=10,
        description="Database connection pool size",
        env="DATABASE_POOL_SIZE",
    )
    database_max_overflow: int = Field(
        default=20,
        description="Database connection pool max overflow",
        env="DATABASE_MAX_OVERFLOW",
    )

    # Service Configuration
    service_name: str = Field(
        default="congressional-data-validation",
        description="Service name for logging and monitoring",
        env="SERVICE_NAME",
    )
    service_version: str = Field(
        default="0.1.0",
        description="Service version",
        env="SERVICE_VERSION",
    )
    service_environment: str = Field(
        default="development",
        description="Environment (development, staging, production)",
        env="SERVICE_ENVIRONMENT",
    )

    # API Configuration
    api_host: str = Field(
        default="0.0.0.0",
        description="API host address",
        env="API_HOST",
    )
    api_port: int = Field(
        default=8002,
        description="API port number",
        env="API_PORT",
    )
    api_workers: int = Field(
        default=1,
        description="Number of API workers",
        env="API_WORKERS",
    )

    # Great Expectations Configuration
    ge_data_context_root: str = Field(
        default="./great_expectations",
        description="Great Expectations data context root directory",
        env="GE_DATA_CONTEXT_ROOT",
    )
    ge_store_backend: str = Field(
        default="filesystem",
        description="Great Expectations store backend (filesystem, s3, gcs)",
        env="GE_STORE_BACKEND",
    )

    # Dagster Configuration
    dagster_home: str = Field(
        default="./dagster_home",
        description="Dagster home directory",
        env="DAGSTER_HOME",
    )
    dagster_postgres_host: Optional[str] = Field(
        default=None,
        description="Dagster postgres host (if using postgres storage)",
        env="DAGSTER_POSTGRES_HOST",
    )
    dagster_postgres_port: int = Field(
        default=5432,
        description="Dagster postgres port",
        env="DAGSTER_POSTGRES_PORT",
    )
    dagster_postgres_db: str = Field(
        default="dagster",
        description="Dagster postgres database name",
        env="DAGSTER_POSTGRES_DB",
    )
    dagster_postgres_user: Optional[str] = Field(
        default=None,
        description="Dagster postgres user",
        env="DAGSTER_POSTGRES_USER",
    )
    dagster_postgres_password: Optional[str] = Field(
        default=None,
        description="Dagster postgres password",
        env="DAGSTER_POSTGRES_PASSWORD",
    )

    # Schema Configuration
    schema_version: str = Field(
        default="v20250708",
        description="Current schema version",
        env="SCHEMA_VERSION",
    )
    staging_schema: str = Field(
        default="staging",
        description="Staging schema name",
        env="STAGING_SCHEMA",
    )
    production_schema: str = Field(
        default="public",
        description="Production schema name",
        env="PRODUCTION_SCHEMA",
    )

    # Pipeline Configuration
    pipeline_batch_size: int = Field(
        default=1000,
        description="Batch size for data processing",
        env="PIPELINE_BATCH_SIZE",
    )
    pipeline_timeout_seconds: int = Field(
        default=3600,
        description="Pipeline execution timeout in seconds",
        env="PIPELINE_TIMEOUT_SECONDS",
    )
    pipeline_retry_attempts: int = Field(
        default=3,
        description="Number of retry attempts for failed operations",
        env="PIPELINE_RETRY_ATTEMPTS",
    )

    # Monitoring Configuration
    enable_metrics: bool = Field(
        default=True,
        description="Enable metrics collection",
        env="ENABLE_METRICS",
    )
    metrics_port: int = Field(
        default=8003,
        description="Metrics server port",
        env="METRICS_PORT",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        env="LOG_LEVEL",
    )

    @validator("service_environment")
    def validate_environment(cls, v: str) -> str:
        """Validate service environment value."""
        allowed_environments = {"development", "staging", "production"}
        if v not in allowed_environments:
            raise ValueError(f"Environment must be one of: {allowed_environments}")
        return v

    @validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level value."""
        allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {allowed_levels}")
        return v.upper()

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.service_environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.service_environment == "development"

    @property
    def versioned_table_suffix(self) -> str:
        """Get versioned table suffix."""
        return f"_{self.schema_version}"


# Global settings instance
settings = Settings()