"""Configuration management for the API service."""

import os
import secrets
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
    rate_limit_burst: int = Field(default=200, description="Rate limit burst allowance")

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
    health_check_timeout: int = Field(default=10, description="Health check timeout")
    
    # Performance Settings
    uvicorn_workers: int = Field(default=4, description="Uvicorn workers")
    uvicorn_worker_class: str = Field(
        default="uvicorn.workers.UvicornWorker", description="Uvicorn worker class"
    )
    uvicorn_max_requests: int = Field(default=1000, description="Max requests per worker")
    uvicorn_max_requests_jitter: int = Field(default=100, description="Max requests jitter")
    
    # Logging
    log_format: str = Field(default="pretty", description="Log format (pretty/json)")
    log_rotation: bool = Field(default=False, description="Enable log rotation")
    log_retention: int = Field(default=30, description="Log retention in days")

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
        default_factory=lambda: secrets.token_urlsafe(32), description="Secret key"
    )
    algorithm: str = Field(default="HS256", description="Algorithm")
    access_token_expire_minutes: int = Field(
        default=30, description="Access token expire minutes"
    )
    
    # Security Headers
    security_headers_enabled: bool = Field(default=True, description="Enable security headers")
    hsts_max_age: int = Field(default=31536000, description="HSTS max age")
    csrf_protection: bool = Field(default=True, description="Enable CSRF protection")

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

    @field_validator("log_format")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        """Validate log format."""
        valid_formats = ["pretty", "json"]
        if v.lower() not in valid_formats:
            raise ValueError(f"Log format must be one of: {valid_formats}")
        return v.lower()

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate secret key."""
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables

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

    @property
    def uvicorn_config(self) -> dict:
        """Get Uvicorn configuration."""
        return {
            "host": self.api_host,
            "port": self.api_port,
            "workers": self.uvicorn_workers if self.is_production else 1,
            "worker_class": self.uvicorn_worker_class,
            "max_requests": self.uvicorn_max_requests,
            "max_requests_jitter": self.uvicorn_max_requests_jitter,
            "reload": self.api_reload and not self.is_production,
        }

    @property
    def security_config(self) -> dict:
        """Get security configuration."""
        return {
            "secret_key": self.secret_key,
            "algorithm": self.algorithm,
            "access_token_expire_minutes": self.access_token_expire_minutes,
            "security_headers_enabled": self.security_headers_enabled,
            "hsts_max_age": self.hsts_max_age,
            "csrf_protection": self.csrf_protection,
        }

    @property
    def rate_limit_config(self) -> dict:
        """Get rate limiting configuration."""
        return {
            "requests": self.rate_limit_requests,
            "period": self.rate_limit_period,
            "burst": self.rate_limit_burst,
        }


# Load settings based on environment
def load_settings() -> Settings:
    """Load settings based on environment."""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    # Determine which env file to load
    env_files = [".env"]
    if env == "production":
        env_files.append(".env.production")
    elif env == "staging":
        env_files.append(".env.staging")
    
    # Load settings with appropriate env file
    for env_file in env_files:
        if Path(env_file).exists():
            return Settings(_env_file=env_file)
    
    return Settings()

# Global settings instance
settings = load_settings()