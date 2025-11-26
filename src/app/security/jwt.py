# src/app/security/jwt.py

from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt

from app.repositories.user_repository import UserRepository
from app.core.config.database import get_session
from app.core.config.settings import settings

auth_scheme = HTTPBearer()
ALGORITHM = "HS256"


def create_access_token(user):
    payload = {
        "sub": user.id,
        "username": user.username,
        "rol": user.rol,
        "password_changed_at": str(user.password_changed_at),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        ),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user):
    payload = {
        "sub": user.id,
        "username": user.username,
        "rol": user.rol,
        "password_changed_at": str(user.password_changed_at),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=30),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(401, "Invalid token")


def get_current_user(token: str = Depends(auth_scheme)):
    token = token.credentials

    data = decode_token(token)

    db = get_session()
    repo = UserRepository(db)

    user = repo.get(data["sub"])
    if not user or not user.is_active:
        raise HTTPException(401, "User invalid or inactive")

    if str(user.password_changed_at) != data.get("password_changed_at"):
        raise HTTPException(401, "Token invalidated by password change")

    return user

# src/app/security/jwt.py
