"""Repository pattern: thin data-access layer.

Repositories encapsulate SQLAlchemy queries so services don't depend directly
on the ORM, making them easier to test and reason about.
"""
from app.repositories.product_repo import ProductRepository
from app.repositories.customer_repo import CustomerRepository
from app.repositories.order_repo import OrderRepository

__all__ = ["ProductRepository", "CustomerRepository", "OrderRepository"]
