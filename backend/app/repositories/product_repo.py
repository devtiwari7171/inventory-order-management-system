"""Product repository: data access for products."""
from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Data access for products."""

    def __init__(self, db: Session) -> None:
        super().__init__(Product, db)

    def get_by_sku(self, sku: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.sku == sku).first()

    def search(self, query: Optional[str], skip: int = 0, limit: int = 100) -> List[Product]:
        """Search products by name or SKU."""
        q = self.db.query(Product)
        if query:
            like = f"%{query}%"
            q = q.filter(or_(Product.name.ilike(like), Product.sku.ilike(like)))
        return q.order_by(Product.id.asc()).offset(skip).limit(limit).all()

    def count_search(self, query: Optional[str]) -> int:
        q = self.db.query(Product)
        if query:
            like = f"%{query}%"
            q = q.filter(or_(Product.name.ilike(like), Product.sku.ilike(like)))
        return q.count()

    def list_low_stock(self, threshold: int = 10) -> List[Product]:
        """Products whose stock is at or below the threshold."""
        return (
            self.db.query(Product)
            .filter(Product.stock_quantity <= threshold)
            .order_by(Product.stock_quantity.asc())
            .all()
        )
