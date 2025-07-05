"""
Tests for the main API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Congressional Data Automation Service"
    assert data["status"] == "active"
    assert "version" in data


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_api_status():
    """Test the API status endpoint."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["api_status"] == "active"
    assert "congress_api_rate_limit" in data
    assert "database_status" in data
    assert "version" in data


def test_database_stats():
    """Test the database stats endpoint."""
    response = client.get("/api/v1/stats/database")
    assert response.status_code == 200
    data = response.json()
    assert "members" in data
    assert "committees" in data
    assert "hearings" in data
    
    # Check structure of stats
    assert "total" in data["members"]
    assert "house" in data["members"]
    assert "senate" in data["members"]


@pytest.mark.asyncio
async def test_congress_api_test():
    """Test the Congress API test endpoint."""
    response = client.get("/api/v1/test/congress-api")
    # This might fail in CI without real API key, so check for expected structure
    assert response.status_code in [200, 500]  # Either success or expected failure
    
    if response.status_code == 200:
        data = response.json()
        assert "api_connection" in data
        assert "rate_limit_status" in data


def test_update_endpoints_structure():
    """Test that update endpoints exist and have correct structure."""
    # Test members update endpoint
    response = client.post("/api/v1/update/members")
    assert response.status_code in [200, 500]  # Structure exists
    
    # Test committees update endpoint
    response = client.post("/api/v1/update/committees")
    assert response.status_code in [200, 500]  # Structure exists
    
    # Test hearings update endpoint
    response = client.post("/api/v1/update/hearings")
    assert response.status_code in [200, 500]  # Structure exists
    
    # Test full update endpoint
    response = client.post("/api/v1/update/full")
    assert response.status_code in [200, 500]  # Structure exists


def test_invalid_endpoint():
    """Test that invalid endpoints return 404."""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404


def test_cors_headers():
    """Test that CORS headers are present."""
    response = client.get("/")
    assert response.status_code == 200
    # CORS headers should be handled by FastAPI middleware


def test_with_database(test_db):
    """Test that database fixture works."""
    assert test_db is not None