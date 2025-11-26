from datetime import datetime
from pydantic import BaseModel

class LoginInput(BaseModel):
    username: str
    password: str
    # TODO captcha_token: str | None = None

class RefreshInput(BaseModel):
    refresh_token: str

class ChangePasswordInput(BaseModel):
    old_password: str
    new_password: str

class MFARequest(BaseModel):
    username: str

class MFAVerify(BaseModel):
    username: str
    code: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    rol: str
    user_language: str | None = None
    user_theme: str | None = None
    is_active: bool
    last_login: datetime | None = None
