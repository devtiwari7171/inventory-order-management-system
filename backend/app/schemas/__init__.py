"""Pydantic schemas (request/response DTOs)."""
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductListResponse,
)
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerListResponse,
)
from app.schemas.order import (
    OrderItemCreate,
    OrderItemResponse,
    OrderCreate,
    OrderResponse,
    OrderListResponse,
)
from app.schemas.dashboard import DashboardStats

__all__ = [
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductListResponse",
    "CustomerCreate",
    "CustomerUpdate",
    "CustomerResponse",
    "CustomerListResponse",
    "OrderItemCreate",
    "OrderItemResponse",
    "OrderCreate",
    "OrderResponse",
    "OrderListResponse",
    "DashboardStats",
]
