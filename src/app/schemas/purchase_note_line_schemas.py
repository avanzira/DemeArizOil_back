# file: src/app/schemas/purchase_note_line_schemas.py

from pydantic import BaseModel, ConfigDict


class PurchaseNoteLineOut(BaseModel):
    id: int
    purchase_id: int
    product_id: int
    quantity: float
    unit_price: float
    line_total: float

    model_config = ConfigDict(from_attributes=True)
