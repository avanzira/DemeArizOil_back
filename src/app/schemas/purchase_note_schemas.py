# file: src/app/schemas/purchase_note_schemas.py

from pydantic import BaseModel, ConfigDict, computed_field
from datetime import datetime
from typing import List
from src.app.schemas.purchase_note_line_schemas import PurchaseNoteLineOut


class LinePurchaseInput(BaseModel):
    product_id: int
    quantity: int
    unit_price: float


class PurchaseNoteCreate(BaseModel):
    supplier_id: int
    account_id: int
    lines: List[LinePurchaseInput]
    paid: float


class PurchaseNoteOut(BaseModel):
    id: int
    supplier_id: int
    account_id: int
    date: datetime
    total: float
    paid: float
    pending: float
    lines: List[PurchaseNoteLineOut]

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def balance(self) -> float:
        return self.pending
