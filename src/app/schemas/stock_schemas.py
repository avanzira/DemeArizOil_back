# file: src/app/schemas/stock_schemas.py
from pydantic import BaseModel, Field

class StockMovementBase(BaseModel):
    product_id: int
    origin_location_id: int | None = None
    destination_location_id: int | None = None
    quantity: int = Field(gt=0)
    movement_type: str

class StockMovementCreate(StockMovementBase):
    purchase_id: int | None = None
    sales_id: int | None = None

class StockMovementOut(StockMovementBase):
    id: int
    purchase_id: int | None
    sales_id: int | None
    is_active: bool
