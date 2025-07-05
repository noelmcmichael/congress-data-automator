"""
Test configuration and fixtures.
"""
import os
import pytest

# Set test environment variables BEFORE importing app modules
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["CONGRESS_API_KEY"] = "test_api_key"
os.environ["SECRET_KEY"] = "test_secret_key"
os.environ["GCP_PROJECT_ID"] = "test_project"
os.environ["DEBUG"] = "true"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base, get_db
from app.main import app


@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal
    
    # Cleanup
    try:
        os.remove("test.db")
    except FileNotFoundError:
        pass