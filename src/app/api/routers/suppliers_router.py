# file: src/app/api/routers/suppliers_router.py
from fastapi import APIRouter, Depends
from src.app.services.suppliers_service import SuppliersService
from src.app.schemas.supplier_schemas import SupplierCreate, SupplierUpdate, SupplierOut
from src.app.security.jwt import get_current_user

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.get("/", response_model=list[SupplierOut])
def list_suppliers(user = Depends(get_current_user)):
    return SuppliersService().list()

@router.get("/{supplier_id}", response_model=SupplierOut)
def get_supplier(supplier_id: int, user = Depends(get_current_user)):
    return SuppliersService().get(supplier_id)

@router.post("/", response_model=SupplierOut)
def create_supplier(data: SupplierCreate, user = Depends(get_current_user)):
    return SuppliersService().create(data)

@router.put("/{supplier_id}", response_model=SupplierOut)
def update_supplier(supplier_id: int, data: SupplierUpdate, user = Depends(get_current_user)):
    return SuppliersService().update(supplier_id, data)

@router.delete("/{supplier_id}", response_model=dict)
def delete_supplier(supplier_id: int, user = Depends(get_current_user)):
    return SuppliersService().delete(supplier_id)