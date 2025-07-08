"""Test main application functionality."""

import pytest
from fastapi.testclient import TestClient

from api.app import create_app
from api.core.config import settings


@pytest.fixture
def app():
    """Create test application."""
    return create_app()


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "congressional_data_api"
    assert data["version"] == settings.api_version


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Congressional Data API"
    assert data["version"] == settings.api_version


def test_detailed_health_endpoint(client):
    """Test detailed health endpoint."""
    response = client.get("/healthz")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "service" in data
    assert "version" in data
    assert "checks" in data
    assert "database" in data["checks"]


def test_openapi_schema(client):
    """Test OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    schema = response.json()
    assert schema["info"]["title"] == settings.api_title
    assert schema["info"]["version"] == settings.api_version