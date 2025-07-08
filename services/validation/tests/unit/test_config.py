"""Test configuration management."""

import pytest
from pydantic import ValidationError

from validation.core.config import Settings


def test_settings_initialization():
    """Test settings initialization with defaults."""
    settings = Settings()
    
    assert settings.service_name == "congressional-data-validation"
    assert settings.service_version == "0.1.0"
    assert settings.service_environment == "development"
    assert settings.api_host == "0.0.0.0"
    assert settings.api_port == 8002
    assert settings.schema_version == "v20250708"
    assert settings.staging_schema == "staging"
    assert settings.production_schema == "public"


def test_settings_validation():
    """Test settings validation."""
    # Valid environment
    settings = Settings(service_environment="production")
    assert settings.service_environment == "production"
    
    # Invalid environment
    with pytest.raises(ValidationError):
        Settings(service_environment="invalid")
    
    # Valid log level
    settings = Settings(log_level="DEBUG")
    assert settings.log_level == "DEBUG"
    
    # Invalid log level
    with pytest.raises(ValidationError):
        Settings(log_level="INVALID")


def test_settings_properties():
    """Test settings properties."""
    dev_settings = Settings(service_environment="development")
    assert dev_settings.is_development is True
    assert dev_settings.is_production is False
    
    prod_settings = Settings(service_environment="production")
    assert prod_settings.is_development is False
    assert prod_settings.is_production is True
    
    assert dev_settings.versioned_table_suffix == "_v20250708"


def test_settings_with_database_url():
    """Test settings with database URL."""
    db_url = "postgresql://user:pass@localhost:5432/test_db"
    settings = Settings(database_url=db_url)
    
    assert settings.database_url == db_url