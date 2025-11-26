# file: src/app/repositories/supplier_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.supplier import Supplier

class SupplierRepository(BaseRepository):
    model = Supplier
