"""Service layer: business logic / use cases.

Services coordinate repositories and enforce business rules.  Keeping logic out
of the API layer keeps routes thin and improves testability.
"""
from app.services.product_service import ProductService
from app.services.customer_service import CustomerService
from app.services.order_service import OrderService

__all__ = ["ProductService", "CustomerService", "OrderService"]
