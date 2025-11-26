# file: src/app/schemas/cash_schemas.py
from pydantic import BaseModel, Field

class CashMovementBase(BaseModel):
    account_from_id: int | None = None
    account_to_id: int | None = None
    amount: float = Field(gt=0)

class CashMovementCreate(CashMovementBase):
    purchase_id: int | None = None
    sales_id: int | None = None

class CashMovementOut(CashMovementBase):
    id: int
    purchase_id: int | None
    sales_id: int | None
    is_active: bool
