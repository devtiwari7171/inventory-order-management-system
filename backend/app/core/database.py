"""Database engine and session configuration."""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


# Engine configuration with pooling for production use
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before use
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)

# Base class for all ORM models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session.

    Ensures proper cleanup via try/finally.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
