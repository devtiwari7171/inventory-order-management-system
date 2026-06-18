"""Base model with common timestamp columns."""
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TimestampMixin:
    """Adds created_at and updated_at columns to a model."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class BaseModel(Base, TimestampMixin):
    """Abstract base for all models with id and timestamps."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
