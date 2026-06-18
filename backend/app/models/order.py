"""Order and OrderItem ORM models.

Order: header record (customer, total, timestamp).
OrderItem: line item belonging to an order, references a product.
"""
from decimal import Decimal
from typing import TYPE_CHECKING, List

from sqlalchemy import CheckConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.product import Product


class Order(BaseModel):
    """An order placed by a customer."""

    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="ck_orders_total_non_negative"),
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )

    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="orders", lazy="joined"
    )
    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Order id={self.id} customer_id={self.customer_id} total={self.total_amount}>"


class OrderItem(Base):
    """A line item within an order."""

    __tablename__ = "order_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_items_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="ck_order_items_unit_price_non_negative"),
        CheckConstraint("subtotal >= 0", name="ck_order_items_subtotal_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")

    def __repr__(self) -> str:
        return (
            f"<OrderItem id={self.id} order_id={self.order_id} "
            f"product_id={self.product_id} qty={self.quantity}>"
        )
