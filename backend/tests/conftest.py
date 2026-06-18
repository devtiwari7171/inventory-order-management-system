"""Test fixtures: in-memory SQLite database and FastAPI test client.

We use SQLite for tests because it's fast and requires no external service.  We
override the dependency that yields DB sessions.
"""
import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configure test environment BEFORE importing the app
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")

from app.core.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402


# In-memory SQLite with shared connection for the test session
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


def override_get_db() -> Generator:
    """Yield a session bound to the test DB."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database() -> Generator:
    """Create fresh tables for each test, then drop them."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a TestClient for the FastAPI app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db() -> Generator:
    """Direct DB session for unit-level tests."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
