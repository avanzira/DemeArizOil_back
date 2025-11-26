# src/app/api/routers/cash_router.py
# Nota: funciones sueltas, services instanciados por endpoint.


from fastapi import APIRouter, Depends
from app.services.cash_service import CashService
from app.security.jwt import get_current_user
from app.schemas.cash_schemas import CashMovementCreate, CashMovementOut

router = APIRouter(prefix="/cash", tags=["cash"])


@router.get("/accounts")
def list_accounts(user = Depends(get_current_user)):
    return CashService().list_accounts()


@router.get("/movements", response_model=list[CashMovementOut])
def list_movements(user = Depends(get_current_user)):
    return CashService().list_movements()


@router.post("/movement", response_model=CashMovementOut | bool)
def create_movement(data: CashMovementCreate, user = Depends(get_current_user)):
    return CashService().register_movement(
        account_from_id=data.account_from_id,
        account_to_id=data.account_to_id,
        amount=data.amount,
        purchase_id=data.purchase_id,
        sales_id=data.sales_id,
    )

# src/app/api/routers/cash_router.py
