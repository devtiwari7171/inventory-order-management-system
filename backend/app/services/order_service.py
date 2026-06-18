"""Order service: the most complex piece.

Business rules:
1. Customer must exist.
2. Each product must exist.
3. Each quantity must be > 0 (enforced by Pydantic).
4. Stock is validated before order creation.
5. Stock is decremented after order creation.
6. Total is computed automatically.
7. All work happens in a single transaction; failure rolls everything back.
"""
from decimal import Decimal
from typing import List

from sqlalchemy.orm import Session

from app.exceptions import BusinessRuleViolation, NotFoundException
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.repositories.customer_repo import CustomerRepository
from app.repositories.order_repo import OrderRepository
from app.repositories.product_repo import ProductRepository
from app.schemas.order import OrderCreate


class OrderService:
    """Orchestrates order creation atomically."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.order_repo = OrderRepository(db)
        self.product_repo = ProductRepository(db)
        self.customer_repo = CustomerRepository(db)

    def list_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        return self.order_repo.list_recent(skip=skip, limit=limit)

    def count_orders(self) -> int:
        return self.order_repo.count()

    def get_order(self, order_id: int) -> Order:
        order = self.order_repo.get_with_items(order_id)
        if not order:
            raise NotFoundException(f"Order with id={order_id} not found")
        return order

    def cancel_order(self, order_id: int) -> None:
        """Cancel (delete) an order and restore inventory atomically.

        Business rule: when an order is cancelled, the stock that was
        deducted during creation is added back so it can be sold again.
        All operations happen inside a single transaction.
        """
        try:
            order = self.order_repo.get_with_items(order_id)
            if not order:
                raise NotFoundException(f"Order with id={order_id} not found")

            # Restore inventory for every line item
            for item in order.items:
                product = self.product_repo.get(item.product_id)
                if product:
                    product.stock_quantity = product.stock_quantity + item.quantity

            self.order_repo.delete(order)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def create_order(self, data: OrderCreate) -> Order:
        """Create an order, decrement stock, and return the persisted order.

        All operations occur inside a single transaction.  If anything fails
        the database rolls back, leaving stock untouched.
        """
        try:
            customer = self.customer_repo.get(data.customer_id)
            if not customer:
                raise NotFoundException(f"Customer with id={data.customer_id} not found")

            # Validate products and stock first (before any writes)
            line_items: list[tuple[Product, int, Decimal]] = []
            for item in data.items:
                product = self.product_repo.get(item.product_id)
                if not product:
                    raise NotFoundException(f"Product with id={item.product_id} not found")
                if item.quantity <= 0:
                    raise BusinessRuleViolation(
                        f"Quantity for product {product.sku} must be greater than 0"
                    )
                if product.stock_quantity < item.quantity:
                    raise BusinessRuleViolation(
                        f"Insufficient stock for product '{product.name}' "
                        f"(SKU: {product.sku}). Available: {product.stock_quantity}, "
                        f"requested: {item.quantity}"
                    )
                # Use supplied price or current product price
                unit_price = item.unit_price if item.unit_price is not None else product.price
                line_items.append((product, item.quantity, unit_price))

            # All validation passed - create order and items
            order = Order(customer_id=customer.id, total_amount=Decimal("0.00"))
            self.db.add(order)
            self.db.flush()  # assign order.id without committing

            total = Decimal("0.00")
            for product, qty, unit_price in line_items:
                subtotal = unit_price * Decimal(qty)
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=qty,
                    unit_price=unit_price,
                    subtotal=subtotal,
                )
                self.db.add(order_item)

                # Decrement inventory
                product.stock_quantity = product.stock_quantity - qty

                total += subtotal

            order.total_amount = total
            self.db.flush()
            self.db.refresh(order)
            self.db.commit()
            return order
        except Exception:
            self.db.rollback()
            raise
