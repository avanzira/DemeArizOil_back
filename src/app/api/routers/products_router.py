# file: src/app/api/routers/products_router.py
from fastapi import APIRouter, Depends
from src.app.services.products_service import ProductsService
from src.app.schemas.product_schemas import ProductCreate, ProductUpdate, ProductOut
from src.app.security.jwt import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductOut])
def list_products(user = Depends(get_current_user)):
    return ProductsService().list()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, user = Depends(get_current_user)):
    return ProductsService().get(product_id)

@router.post("/", response_model=ProductOut)
def create_product(data: ProductCreate, user = Depends(get_current_user)):
    return ProductsService().create(data)

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate, user = Depends(get_current_user)):
    return ProductsService().update(product_id, data)

@router.delete("/{product_id}", response_model=dict)
def delete_product(product_id: int, user = Depends(get_current_user)):
    return ProductsService().delete(product_id)