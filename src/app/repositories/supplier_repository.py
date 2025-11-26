# file: src/app/repositories/supplier_repository.py
from app.repositories.base import BaseRepository
from app.models.supplier import Supplier

class SupplierRepository(BaseRepository):
    model = Supplier
