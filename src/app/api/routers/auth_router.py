# file: src/app/routers/auth_router.py

from fastapi import APIRouter, Depends, Request
from src.app.schemas.auth_schemas import LoginInput, RefreshInput, ChangePasswordInput
from src.app.services.auth_service import AuthService
from src.app.security.jwt import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(data: LoginInput, request: Request):
    return AuthService().login(data, client_ip=request.client.host)

@router.post("/refresh")
def refresh(data: RefreshInput):
    return AuthService().refresh(data)

@router.post("/change-password")
def change_password(data: ChangePasswordInput, user=Depends(get_current_user)):
    return AuthService().change_password(user, data)

@router.get("/me")
def me(user=Depends(get_current_user)):
    return AuthService().me(user)
