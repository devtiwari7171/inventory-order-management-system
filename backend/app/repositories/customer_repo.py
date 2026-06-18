"""Customer repository."""
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.base import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self, db: Session) -> None:
        super().__init__(Customer, db)

    def get_by_email(self, email: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(Customer.email == email).first()

    def search(self, query: Optional[str], skip: int = 0, limit: int = 100) -> List[Customer]:
        q = self.db.query(Customer)
        if query:
            like = f"%{query}%"
            q = q.filter(or_(Customer.name.ilike(like), Customer.email.ilike(like)))
        return q.order_by(Customer.id.asc()).offset(skip).limit(limit).all()

    def count_search(self, query: Optional[str]) -> int:
        q = self.db.query(Customer)
        if query:
            like = f"%{query}%"
            q = q.filter(or_(Customer.name.ilike(like), Customer.email.ilike(like)))
        return q.count()
