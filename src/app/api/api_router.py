# file: src/app/api/api_router.py
from fastapi import APIRouter

from app.api.routers.products_router import router as products_router
from app.api.routers.customers_router import router as customers_router
from app.api.routers.suppliers_router import router as suppliers_router
from app.api.routers.stock_router import router as stock_router
from app.api.routers.cash_router import router as cash_router
from app.api.routers.purchase_notes_router import router as purchase_notes_router
from app.api.routers.sales_notes_router import router as sales_notes_router
from app.api.routers.users_router import router as users_router
from app.api.routers.auth_router import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(products_router)
api_router.include_router(customers_router)
api_router.include_router(suppliers_router)
api_router.include_router(stock_router)
api_router.include_router(cash_router)
api_router.include_router(purchase_notes_router)
api_router.include_router(sales_notes_router)
