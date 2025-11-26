# file: src/app/schemas/customer_schemas.py
from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None

class CustomerOut(CustomerBase):
    id: int
    is_active: bool
