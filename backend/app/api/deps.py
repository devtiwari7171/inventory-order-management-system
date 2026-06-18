"""Dependency injection providers.

Routes depend on these helpers which in turn construct services with a DB
session.  Services can then be swapped for mocks in tests.
"""
from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.customer_service import CustomerService
from app.services.order_service import OrderService
from app.services.product_service import ProductService


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db)


def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(db)


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db)
