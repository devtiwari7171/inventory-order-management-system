"""Pydantic schemas for products."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductBase(BaseModel):
    """Common product fields."""

    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    sku: str = Field(..., min_length=1, max_length=64, description="Unique stock-keeping unit")
    price: Decimal = Field(..., ge=0, description="Product price (cannot be negative)")
    stock_quantity: int = Field(..., ge=0, description="Available stock (cannot be negative)")

    @field_validator("name", "sku")
    @classmethod
    def strip_strings(cls, v: str) -> str:
        return v.strip()


class ProductCreate(ProductBase):
    """Schema for creating a product."""

    pass


class ProductUpdate(BaseModel):
    """Schema for partial product updates (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sku: Optional[str] = Field(None, min_length=1, max_length=64)
    price: Optional[Decimal] = Field(None, ge=0)
    stock_quantity: Optional[int] = Field(None, ge=0)

    @field_validator("name", "sku")
    @classmethod
    def strip_strings(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v


class ProductResponse(ProductBase):
    """Schema returned to clients."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    """Paginated product list."""

    items: List[ProductResponse]
    total: int
