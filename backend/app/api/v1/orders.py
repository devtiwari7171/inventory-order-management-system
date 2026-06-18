"""Order endpoints."""
from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_order_service
from app.schemas.order import OrderCreate, OrderListResponse, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an order (validates & decrements stock atomically)",
)
def create_order(
    payload: OrderCreate,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    return OrderResponse.model_validate(service.create_order(payload))


@router.get(
    "/",
    response_model=OrderListResponse,
    summary="List recent orders",
)
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    service: OrderService = Depends(get_order_service),
) -> OrderListResponse:
    items = service.list_orders(skip=skip, limit=limit)
    total = service.count_orders()
    return OrderListResponse(
        items=[OrderResponse.model_validate(o) for o in items],
        total=total,
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Get order by id (with items)",
)
def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    return OrderResponse.model_validate(service.get_order(order_id))


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel/delete an order (restores stock)",
)
def cancel_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
) -> None:
    """Cancel an order. Stock is restored automatically."""
    service.cancel_order(order_id)
    return None
