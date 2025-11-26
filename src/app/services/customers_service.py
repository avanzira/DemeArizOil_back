# file: src/app/services/customers_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services.base_service import BaseService
from app.core.enums.stock_enums import StockLocationType
from app.repositories.customer_repository import CustomerRepository
from app.repositories.stock_location_repository import StockLocationRepository
from app.repositories.stock_product_location_repository import StockProductLocationRepository
from app.schemas.customer_schemas import CustomerCreate, CustomerUpdate

class CustomersService(BaseService):
    repo_class = CustomerRepository

    def __init__(self, db: Session | None = None):
        super().__init__(db)
        self.locations = StockLocationRepository(self.db)
        self.rows = StockProductLocationRepository(self.db)

    def create(self, schema: CustomerCreate):
        name = schema.name.strip()
        if not name:
            raise HTTPException(400, "Customer name cannot be empty")

        if self.db.query(self.repo.model).filter_by(name=name).first():
            raise HTTPException(400, "Customer already exists")

        customer = super().create({
            "name": name,
            "phone": schema.phone,
            "email": schema.email,
            "address": schema.address
        })

        self.locations.create({
            "name": f"customer_{customer.id}_stock",
            "type": StockLocationType.CUSTOMER
        })

        return customer

    def update(self, id: int, schema: CustomerUpdate):
        customer = self._get_or_404(id)
        updates = {}

        if schema.name is not None:
            nm = schema.name.strip()
            if not nm:
                raise HTTPException(400, "Customer name cannot be empty")
            updates["name"] = nm

        if schema.phone is not None:
            updates["phone"] = schema.phone
        if schema.email is not None:
            updates["email"] = schema.email
        if schema.address is not None:
            updates["address"] = schema.address

        updated = self.repo.update(customer, updates)
        return updated

    def delete(self, id: int):
        customer = self._get_or_404(id)

        loc = self.db.query(self.locations.model).filter_by(
            name=f"customer_{customer.id}_stock"
        ).first()

        if not loc:
            raise HTTPException(500, "Customer stock location missing")

        rows = self.db.query(self.rows.model).filter_by(location_id=loc.id).all()
        total_stock = sum(r.quantity for r in rows)

        if total_stock > 0:
            raise HTTPException(400, "Cannot delete customer with non-empty deposit")

        super().delete(id)
        return {"id": customer.id, "deleted": true}