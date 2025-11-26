# file: src/app/api/routers/stock_router.py
# Nota: este router sigue la recomendación oficial de FastAPI
# usando funciones sueltas sin clases y services por endpoint.

from fastapi import APIRouter, Depends
from app.services.stock_service import StockService
from app.security.jwt import get_current_user

router = APIRouter(prefix="/stock", tags=["stock"])

@router.get("/locations")
def list_locations(user = Depends(get_current_user)):
    return StockService().list_locations()

@router.get("/product/{product_id}")
def get_stock_by_product(product_id: int, user = Depends(get_current_user)):
    return StockService().get_stock_by_product(product_id)

@router.get("/total/{product_id}")
def get_stock_total(product_id: int, user = Depends(get_current_user)):
    return StockService().get_stock_total(product_id)
