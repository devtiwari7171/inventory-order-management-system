"""Pydantic schemas for orders and order items."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OrderItemBase(BaseModel):
    """Base order-item fields."""

    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, description="Must be greater than zero")


class OrderItemCreate(OrderItemBase):
    """Schema for creating an order item.

    unit_price is optional - if not supplied, the current product price is used.
    """

    unit_price: Optional[Decimal] = Field(
        None, ge=0, description="Override price; defaults to product price"
    )


class OrderItemResponse(BaseModel):
    """Schema returned to clients."""

    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    """Schema for creating an order."""

    customer_id: int = Field(..., gt=0)
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderResponse(BaseModel):
    """Schema returned to clients for an order."""

    id: int
    customer_id: int
    total_amount: Decimal
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(BaseModel):
    """Paginated order list."""

    items: List[OrderResponse]
    total: int
