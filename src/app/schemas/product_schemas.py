# file: src/app/schemas/product_schemas.py
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    unit_measure: str
    is_inventory: bool


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    unit_measure: str | None = None
    is_inventory: bool | None = None
    

class ProductOut(ProductBase):
    id: int
    cost_average: float
    is_active: bool
