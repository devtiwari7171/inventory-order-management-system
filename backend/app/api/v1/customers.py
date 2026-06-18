"""Customer endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_customer_service
from app.schemas.customer import (
    CustomerCreate,
    CustomerListResponse,
    CustomerResponse,
    CustomerUpdate,
)
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a customer",
)
def create_customer(
    payload: CustomerCreate,
    service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    return CustomerResponse.model_validate(service.create_customer(payload))


@router.get(
    "/",
    response_model=CustomerListResponse,
    summary="List customers (with optional search)",
)
def list_customers(
    q: Optional[str] = Query(None, description="Search by name or email"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    service: CustomerService = Depends(get_customer_service),
) -> CustomerListResponse:
    items = service.list_customers(query=q, skip=skip, limit=limit)
    total = service.count_customers(query=q)
    return CustomerListResponse(
        items=[CustomerResponse.model_validate(c) for c in items],
        total=total,
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Get customer by id",
)
def get_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    return CustomerResponse.model_validate(service.get_customer(customer_id))


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Update customer",
)
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    service: CustomerService = Depends(get_customer_service),
) -> CustomerResponse:
    return CustomerResponse.model_validate(service.update_customer(customer_id, payload))


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete customer",
)
def delete_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service),
) -> None:
    service.delete_customer(customer_id)
    return None
