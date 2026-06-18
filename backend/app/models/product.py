"""Product ORM model."""
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import CheckConstraint, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.order import OrderItem


class Product(BaseModel):
    """A product in the inventory catalog."""

    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("sku", name="uq_products_sku"),
        CheckConstraint("price >= 0", name="ck_products_price_non_negative"),
        CheckConstraint(
            "stock_quantity >= 0", name="ck_products_stock_non_negative"
        ),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(default=0, nullable=False)

    # Relationship: a product can appear in many order items
    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Product id={self.id} sku={self.sku} name={self.name!r}>"
