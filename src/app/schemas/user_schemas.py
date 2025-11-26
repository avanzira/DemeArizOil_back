# file: src/app/schemas/user_schemas.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    rol: str
    user_language: str | None = None
    user_theme: str | None = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    rol: str = "user"

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    rol: str | None = None
    user_language: str | None = None
    user_theme: str | None = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    rol: str
    is_active: bool
    user_language: str | None
    user_theme: str | None

class ChangePasswordAdmin(BaseModel):
    new_password: str

class UpdatePreferences(BaseModel):
    user_language: str | None
    user_theme: str | None
