# file: src/app/api/routers/users_router.py
# Nota: funciones sueltas por recomendación oficial de FastAPI.

from fastapi import APIRouter, Depends
from src.app.services.user_service import UserService
from src.app.schemas.user_schemas import UserCreate, UserUpdate, ChangePasswordAdmin, UpdatePreferences
from src.app.security.jwt import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users(current_user = Depends(get_current_user)):
    return UserService().list(current_user)

@router.get("/{user_id}")
def get_user(user_id: int, current_user = Depends(get_current_user)):
    return UserService().get(user_id)

@router.post("/")
def create_user(data: UserCreate, current_user = Depends(get_current_user)):
    return UserService().create(data, current_user)

@router.put("/{user_id}")
def update_user(user_id: int, data: UserUpdate, current_user = Depends(get_current_user)):
    return UserService().update(user_id, data, current_user)

@router.delete("/{user_id}")
def delete_user(user_id: int, current_user = Depends(get_current_user)):
    return UserService().delete(user_id, current_user)

@router.post("/{user_id}/change-password")
def change_password_admin(user_id: int, data: ChangePasswordAdmin, current_user = Depends(get_current_user)):
    return UserService().change_password_admin(user_id, data, current_user)

@router.post("/me/preferences")
def update_preferences(data: UpdatePreferences, current_user = Depends(get_current_user)):
    return UserService().update_preferences(current_user.id, data)
