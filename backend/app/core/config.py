"""
Core configuration settings for the Congressional Data Automation Service.
"""
import os
from typing import Optional, List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Congressional Data Automation Service"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    
    # API
    api_v1_prefix: str = "/api/v1"
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_echo: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Congress.gov API
    congress_api_key: str = Field(..., env="CONGRESS_API_KEY")
    congress_api_base_url: str = "https://api.congress.gov/v3"
    congress_api_rate_limit: int = 5000  # requests per day
    congress_api_request_delay: float = 1.0  # seconds between requests
    
    # Web scraping
    scraping_delay: float = 1.0  # seconds between requests
    scraping_timeout: int = 30  # seconds
    scraping_user_agent: str = "Congressional Data Automator (https://github.com/noelmcmichael/congress-data-automator)"
    
    # Authentication
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google Cloud Platform
    gcp_project_id: str = Field(..., env="GCP_PROJECT_ID")
    gcp_location: str = Field(default="us-central1", env="GCP_LOCATION")
    
    # Redis (for caching and background jobs)
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # CORS
    allowed_origins: List[str] = Field(default=["*"], env="ALLOWED_ORIGINS")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Data update schedules (cron format)
    members_update_schedule: str = "0 2 1 * *"  # Monthly at 2 AM on 1st
    committees_update_schedule: str = "0 2 * * 1"  # Weekly on Monday at 2 AM
    hearings_update_schedule: str = "0 */6 * * *"  # Every 6 hours
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()