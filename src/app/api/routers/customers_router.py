# file: src/app/api/routers/customers_router.py
from fastapi import APIRouter, Depends
from src.app.services.customers_service import CustomersService
from src.app.schemas.customer_schemas import CustomerCreate, CustomerUpdate, CustomerOut
from src.app.security.jwt import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/", response_model=list[CustomerOut])
def list_customers(user = Depends(get_current_user)):
    return CustomersService().list()

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, user = Depends(get_current_user)):
    return CustomersService().get(customer_id)

@router.post("/", response_model=CustomerOut)
def create_customer(data: CustomerCreate, user = Depends(get_current_user)):
    return CustomersService().create(data)

@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, data: CustomerUpdate, user = Depends(get_current_user)):
    return CustomersService().update(customer_id, data)

@router.delete("/{customer_id}", response_model=dict)
def delete_customer(customer_id: int, user = Depends(get_current_user)):
    return CustomersService().delete(customer_id)