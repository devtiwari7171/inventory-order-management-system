"""Product endpoints."""
from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_product_service
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a product",
)
def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return ProductResponse.model_validate(service.create_product(payload))


@router.get(
    "/",
    response_model=ProductListResponse,
    summary="List products (with optional search)",
)
def list_products(
    q: Optional[str] = Query(None, description="Search by name or SKU"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    service: ProductService = Depends(get_product_service),
) -> ProductListResponse:
    items = service.list_products(query=q, skip=skip, limit=limit)
    total = service.count_products(query=q)
    return ProductListResponse(
        items=[ProductResponse.model_validate(p) for p in items],
        total=total,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by id",
)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return ProductResponse.model_validate(service.get_product(product_id))


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    service: ProductService = Depends(get_product_service),
) -> ProductResponse:
    return ProductResponse.model_validate(service.update_product(product_id, payload))


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> None:
    service.delete_product(product_id)
    return None
