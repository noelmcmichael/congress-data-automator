"""Configuration management for the API service."""

import os
from pathlib import Path
from typing import List, Optional

from pydantic import Field, field_validator, ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database Configuration
    database_url: str = Field(
        default="postgresql://test:test@localhost:5432/test_db",
        description="Database connection URL",
    )
    database_pool_size: int = Field(default=20, description="Database pool size")
    database_max_overflow: int = Field(
        default=10, description="Database max overflow"
    )
    database_pool_timeout: int = Field(
        default=30, description="Database pool timeout"
    )

    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8003, description="API port")
    api_workers: int = Field(default=4, description="API workers")
    api_reload: bool = Field(default=False, description="API reload")

    # Environment
    environment: str = Field(default="development", description="Environment")
    log_level: str = Field(default="INFO", description="Log level")
    debug: bool = Field(default=False, description="Debug mode")

    # CORS Configuration
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "https://storage.googleapis.com",
        ],
        description="CORS origins",
    )
    cors_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE"],
        description="CORS methods",
    )
    cors_headers: List[str] = Field(default=["*"], description="CORS headers")

    # Redis Configuration
    redis_url: str = Field(
        default="redis://localhost:6379/0", description="Redis URL"
    )
    redis_timeout: int = Field(default=5, description="Redis timeout")
    redis_max_connections: int = Field(
        default=20, description="Redis max connections"
    )

    # Rate Limiting
    rate_limit_requests: int = Field(default=100, description="Rate limit requests")
    rate_limit_period: int = Field(default=60, description="Rate limit period")

    # Pagination
    default_page_size: int = Field(default=20, description="Default page size")
    max_page_size: int = Field(default=100, description="Max page size")

    # Caching
    cache_ttl: int = Field(default=3600, description="Cache TTL")
    cache_enabled: bool = Field(default=True, description="Cache enabled")

    # Monitoring
    metrics_enabled: bool = Field(default=True, description="Metrics enabled")
    health_check_interval: int = Field(
        default=30, description="Health check interval"
    )

    # API Versioning
    api_version_prefix: str = Field(default="/api/v1", description="API version prefix")
    api_title: str = Field(default="Congressional Data API", description="API title")
    api_description: str = Field(
        default="Enterprise-grade read-only API for congressional data",
        description="API description",
    )
    api_version: str = Field(default="1.0.0", description="API version")

    # Security
    secret_key: str = Field(
        default="your-secret-key-here", description="Secret key"
    )
    algorithm: str = Field(default="HS256", description="Algorithm")
    access_token_expire_minutes: int = Field(
        default=30, description="Access token expire minutes"
    )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL."""
        valid_prefixes = ("postgresql://", "postgres://", "sqlite://", "sqlite:///")
        if not v.startswith(valid_prefixes):
            raise ValueError("Database URL must be a PostgreSQL or SQLite connection string")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of: {valid_levels}")
        return v.upper()

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment."""
        valid_environments = ["development", "staging", "production"]
        if v.lower() not in valid_environments:
            raise ValueError(f"Environment must be one of: {valid_environments}")
        return v.lower()

    @field_validator("api_port")
    @classmethod
    def validate_api_port(cls, v: int) -> int:
        """Validate API port."""
        if not (1024 <= v <= 65535):
            raise ValueError("API port must be between 1024 and 65535")
        return v

    @field_validator("default_page_size", "max_page_size")
    @classmethod
    def validate_page_size(cls, v: int) -> int:
        """Validate page size."""
        if v <= 0:
            raise ValueError("Page size must be positive")
        return v

    @field_validator("max_page_size")
    @classmethod
    def validate_max_page_size_limit(cls, v: int, info: ValidationInfo) -> int:
        """Validate max page size is greater than default."""
        if info.data and "default_page_size" in info.data and v < info.data["default_page_size"]:
            raise ValueError("Max page size must be greater than default page size")
        return v

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        """Check if environment is production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if environment is development."""
        return self.environment == "development"

    @property
    def is_staging(self) -> bool:
        """Check if environment is staging."""
        return self.environment == "staging"

    @property
    def database_config(self) -> dict:
        """Get database configuration."""
        return {
            "url": self.database_url,
            "pool_size": self.database_pool_size,
            "max_overflow": self.database_max_overflow,
            "pool_timeout": self.database_pool_timeout,
        }

    @property
    def redis_config(self) -> dict:
        """Get Redis configuration."""
        return {
            "url": self.redis_url,
            "timeout": self.redis_timeout,
            "max_connections": self.redis_max_connections,
        }

    @property
    def cors_config(self) -> dict:
        """Get CORS configuration."""
        return {
            "origins": self.cors_origins,
            "methods": self.cors_methods,
            "headers": self.cors_headers,
        }


# Global settings instance
settings = Settings()