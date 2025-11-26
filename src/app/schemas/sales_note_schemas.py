# file: src/app/schemas/sales_note_schemas.py
from pydantic import BaseModel
from typing import List

class LineSalesInput(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class SalesNoteCreate(BaseModel):
    customer_id: int
    account_id: int
    lines: List[LineSalesInput]

class SalesNoteOut(BaseModel):
    id: int
    customer_id: int
    account_id: int
    total: float
    paid: float
    is_active: bool
