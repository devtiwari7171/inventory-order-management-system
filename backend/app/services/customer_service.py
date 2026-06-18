"""Customer service."""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.exceptions import BusinessRuleViolation, ConflictException, NotFoundException
from app.models.customer import Customer
from app.repositories.customer_repo import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    def __init__(self, db: Session) -> None:
        self.repo = CustomerRepository(db)

    def list_customers(self, query: Optional[str], skip: int = 0, limit: int = 100) -> List[Customer]:
        return self.repo.search(query=query, skip=skip, limit=limit)

    def count_customers(self, query: Optional[str]) -> int:
        return self.repo.count_search(query=query)

    def get_customer(self, customer_id: int) -> Customer:
        customer = self.repo.get(customer_id)
        if not customer:
            raise NotFoundException(f"Customer with id={customer_id} not found")
        return customer

    def create_customer(self, data: CustomerCreate) -> Customer:
        if self.repo.get_by_email(data.email):
            raise ConflictException(f"Customer with email '{data.email}' already exists")
        customer = Customer(name=data.name, email=data.email, phone=data.phone)
        return self.repo.create(customer)

    def update_customer(self, customer_id: int, data: CustomerUpdate) -> Customer:
        customer = self.get_customer(customer_id)
        updates = data.model_dump(exclude_unset=True)
        if "email" in updates and updates["email"] != customer.email:
            if self.repo.get_by_email(updates["email"]):
                raise ConflictException(f"Customer with email '{updates['email']}' already exists")
        return self.repo.update(customer, updates)

    def delete_customer(self, customer_id: int) -> None:
        customer = self.get_customer(customer_id)
        if customer.orders:
            raise BusinessRuleViolation("Cannot delete a customer with existing orders")
        self.repo.delete(customer)
