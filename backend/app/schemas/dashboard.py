"""Dashboard stats schema."""
from typing import List

from pydantic import BaseModel

from app.schemas.product import ProductResponse


class DashboardStats(BaseModel):
    """Aggregated metrics for the dashboard page."""

    total_products: int
    total_customers: int
    total_orders: int
    low_stock_products: List[ProductResponse]
