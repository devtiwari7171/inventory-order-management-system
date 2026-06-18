"""Dashboard aggregate endpoint."""
from fastapi import APIRouter, Depends

from app.api.deps import get_customer_service, get_order_service, get_product_service
from app.schemas.dashboard import DashboardStats
from app.schemas.product import ProductResponse
from app.services.customer_service import CustomerService
from app.services.order_service import OrderService
from app.services.product_service import ProductService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/",
    response_model=DashboardStats,
    summary="Aggregated dashboard metrics",
)
def get_dashboard_stats(
    product_service: ProductService = Depends(get_product_service),
    customer_service: CustomerService = Depends(get_customer_service),
    order_service: OrderService = Depends(get_order_service),
) -> DashboardStats:
    low_stock = product_service.get_low_stock()
    return DashboardStats(
        total_products=product_service.count_products(query=None),
        total_customers=customer_service.count_customers(query=None),
        total_orders=order_service.count_orders(),
        low_stock_products=[ProductResponse.model_validate(p) for p in low_stock],
    )
