"""Product service: business rules around products."""
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from app.exceptions import ConflictException, NotFoundException, ValidationException
from app.models.product import Product
from app.repositories.product_repo import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Encapsulates product-related use cases."""

    LOW_STOCK_THRESHOLD = 10

    def __init__(self, db: Session) -> None:
        self.repo = ProductRepository(db)

    def list_products(self, query: Optional[str], skip: int = 0, limit: int = 100) -> List[Product]:
        return self.repo.search(query=query, skip=skip, limit=limit)

    def count_products(self, query: Optional[str]) -> int:
        return self.repo.count_search(query=query)

    def get_product(self, product_id: int) -> Product:
        product = self.repo.get(product_id)
        if not product:
            raise NotFoundException(f"Product with id={product_id} not found")
        return product

    def create_product(self, data: ProductCreate) -> Product:
        # Business rule: unique SKU
        if self.repo.get_by_sku(data.sku):
            raise ConflictException(f"Product with SKU '{data.sku}' already exists")
        # Defensive validation (Pydantic already enforces non-negative values)
        if data.price < 0:
            raise ValidationException("Price cannot be negative")
        if data.stock_quantity < 0:
            raise ValidationException("Stock cannot be negative")

        product = Product(
            name=data.name,
            sku=data.sku,
            price=data.price,
            stock_quantity=data.stock_quantity,
        )
        return self.repo.create(product)

    def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        product = self.get_product(product_id)
        updates = data.model_dump(exclude_unset=True)

        if "sku" in updates and updates["sku"] != product.sku:
            if self.repo.get_by_sku(updates["sku"]):
                raise ConflictException(f"Product with SKU '{updates['sku']}' already exists")

        if "price" in updates and Decimal(str(updates["price"])) < 0:
            raise ValidationException("Price cannot be negative")
        if "stock_quantity" in updates and updates["stock_quantity"] < 0:
            raise ValidationException("Stock cannot be negative")

        return self.repo.update(product, updates)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        # Restrict delete if product appears in any order
        if product.order_items:
            raise ValidationException(
                "Cannot delete product that has existing order history"
            )
        self.repo.delete(product)

    def get_low_stock(self, threshold: int = LOW_STOCK_THRESHOLD) -> List[Product]:
        return self.repo.list_low_stock(threshold)
