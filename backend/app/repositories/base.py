"""Generic base repository with common CRUD operations."""
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Generic CRUD operations for any model."""

    def __init__(self, model: Type[ModelType], db: Session) -> None:
        self.model = model
        self.db = db

    def get(self, id: int) -> Optional[ModelType]:
        """Fetch a record by primary key."""
        return self.db.get(self.model, id)

    def list(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Return paginated records ordered by id."""
        return (
            self.db.query(self.model)
            .order_by(self.model.id.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self) -> int:
        """Total record count."""
        return self.db.query(self.model).count()

    def create(self, obj: ModelType) -> ModelType:
        """Persist a new record. Commits so the change survives the request."""
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        self.db.commit()
        return obj

    def update(self, obj: ModelType, data: dict) -> ModelType:
        """Apply dict updates to a record. Commits so the change survives the request."""
        for key, value in data.items():
            setattr(obj, key, value)
        self.db.flush()
        self.db.refresh(obj)
        self.db.commit()
        return obj

    def delete(self, obj: ModelType) -> None:
        """Delete a record. Commits so the change survives the request."""
        self.db.delete(obj)
        self.db.flush()
        self.db.commit()
