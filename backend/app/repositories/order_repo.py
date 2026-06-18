"""Order repository."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.order import Order
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self, db: Session) -> None:
        super().__init__(Order, db)

    def list_for_customer(self, customer_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        return (
            self.db.query(Order)
            .filter(Order.customer_id == customer_id)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def list_recent(self, skip: int = 0, limit: int = 100) -> List[Order]:
        return (
            self.db.query(Order)
            .order_by(Order.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_with_items(self, order_id: int) -> Optional[Order]:
        return (
            self.db.query(Order)
            .options()  # relationships use lazy="selectin"
            .filter(Order.id == order_id)
            .first()
        )

    def delete(self, obj: Order) -> None:
        """Delete an order (cascades to order_items via FK)."""
        self.db.delete(obj)
        self.db.flush()
        self.db.commit()
