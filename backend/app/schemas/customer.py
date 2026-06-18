"""Pydantic schemas for customers."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CustomerBase(BaseModel):
    """Common customer fields."""

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=32)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()

    @field_validator("phone")
    @classmethod
    def strip_phone(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v


class CustomerCreate(CustomerBase):
    """Schema for creating a customer."""

    pass


class CustomerUpdate(BaseModel):
    """Partial update."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=32)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v

    @field_validator("phone")
    @classmethod
    def strip_phone(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else v


class CustomerResponse(CustomerBase):
    """Schema returned to clients."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerListResponse(BaseModel):
    """Paginated customer list."""

    items: List[CustomerResponse]
    total: int
