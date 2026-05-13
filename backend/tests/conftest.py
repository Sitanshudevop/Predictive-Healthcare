"""
Shared test fixtures — in-memory SQLite, TestClient.
No auth fixtures needed (authentication has been removed).
"""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

# Override settings BEFORE importing the app
os.environ["DATABASE_URL"] = "sqlite:///./test_phs.db"
os.environ["DEBUG"] = "false"

from app.db.base import Base
from app.db.session import get_db
from app.main import app

# Test database
TEST_DATABASE_URL = "sqlite:///./test_phs.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables once for the test session."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
    # Dispose all connections before removing file (required on Windows)
    test_engine.dispose()
    if os.path.exists("test_phs.db"):
        os.remove("test_phs.db")


@pytest.fixture()
def db_session():
    """Provide a database session for each test."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    """FastAPI TestClient — all endpoints are publicly accessible."""
    return TestClient(app)
