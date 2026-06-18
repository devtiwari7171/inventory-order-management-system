"""SQLAlchemy ORM models.

Database design:
- products: catalog of sellable items
- customers: people who place orders
- orders: header record for a purchase
- order_items: line items belonging to an order

Relationships:
    Customer (1) ──── (N) Order
    Order    (1) ──── (N) OrderItem
    Product  (1) ──── (N) OrderItem
"""
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order, OrderItem

__all__ = ["Product", "Customer", "Order", "OrderItem"]
