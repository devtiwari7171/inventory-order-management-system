"""Customer ORM model."""
from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.order import Order


class Customer(BaseModel):
    """A customer who can place orders."""

    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)

    # One-to-many: a customer has many orders
    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="customer",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Customer id={self.id} email={self.email}>"
