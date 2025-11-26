# file: src/app/services/suppliers_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.app.services.base_service import BaseService
from src.app.repositories.supplier_repository import SupplierRepository
from src.app.repositories.purchase_note_repository import PurchaseNoteRepository
from src.app.schemas.supplier_schemas import SupplierCreate, SupplierUpdate

class SuppliersService(BaseService):
    repo_class = SupplierRepository

    def __init__(self, db: Session | None = None):
        super().__init__(db)
        self.purchase_notes = PurchaseNoteRepository(self.db)

    def create(self, schema: SupplierCreate):
        name = schema.name.strip()
        if not name:
            raise HTTPException(400, "Supplier name cannot be empty")

        if self.db.query(self.repo.model).filter_by(name=name).first():
            raise HTTPException(400, "Supplier already exists")

        supplier = super().create({
            "name": name,
            "phone": schema.phone,
            "email": schema.email,
            "address": schema.address
        })

        return supplier

    def update(self, id: int, schema: SupplierUpdate):
        supplier = self._get_or_404(id)
        updates = {}

        if schema.name is not None:
            nm = schema.name.strip()
            if not nm:
                raise HTTPException(400, "Supplier name cannot be empty")
            updates["name"] = nm

        if schema.phone is not None:
            updates["phone"] = schema.phone
        if schema.email is not None:
            updates["email"] = schema.email
        if schema.address is not None:
            updates["address"] = schema.address

        updated = self.repo.update(supplier, updates)
        return updated

    def delete(self, id: int):
        supplier = self._get_or_404(id)

        notes = self.db.query(self.purchase_notes.model).filter_by(supplier_id=id, is_active=True).all()

        total_pending = sum(float(p.pending) for p in notes)

        if total_pending > 0:
            raise HTTPException(400, "Cannot delete supplier with pending debt")

        super().delete(id)
        return {"id": supplier.id, "deleted": true}