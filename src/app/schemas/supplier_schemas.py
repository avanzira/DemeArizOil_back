# file: src/app/schemas/supplier_schemas.py
from pydantic import BaseModel

class SupplierBase(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None

class SupplierOut(SupplierBase):
    id: int
    is_active: bool
