# src/app/services/auth_service.py

from datetime import datetime
from fastapi import HTTPException

from src.app.repositories.user_repository import UserRepository
from src.app.core.config.database import get_session

from src.app.security.password import verify_password, hash_password

from src.app.schemas.auth_schemas import (
    LoginInput, RefreshInput, ChangePasswordInput,
    MFARequest, MFAVerify, UserOut
)
from src.app.security.captcha import validate_captcha
from src.app.security.rate_limit import check_rate_limit
from src.app.security.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token
)
from src.app.security.mfa import generate_mfa_code


class AuthService:
    def __init__(self):
        self.db = get_session()
        self.repo = UserRepository(self.db)

    def login(self, schema: LoginInput, client_ip: str = "0.0.0.0"):
        # TODO captcha
        # if schema.captcha_token and not validate_captcha(schema.captcha_token):
        #     raise HTTPException(401, "Invalid captcha")

        # TODO rate limit
        # if not check_rate_limit(client_ip):
        #     raise HTTPException(429, "Too many attempts")

        user = self.repo.get_by_username(schema.username)
        if not user or not verify_password(schema.password, user.hash_password):
            raise HTTPException(401, "Invalid credentials")

        if not user.is_active:
            raise HTTPException(403, "User inactive")

        access = create_access_token(user)
        refresh = create_refresh_token(user)

        user.last_login = datetime.utcnow()
        self.db.commit()

        user_out = UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            rol=user.rol,
            user_language=user.user_language,
            user_theme=user.user_theme,
            is_active=user.is_active,
            last_login=user.last_login
        )

        return {
            "access_token": access,
            "refresh_token": refresh,
            "user": user_out.model_dump()
        }

    def refresh(self, schema: RefreshInput):
        payload = decode_token(schema.refresh_token)

        user = self.repo.get(payload["sub"])
        if not user or not user.is_active:
            raise HTTPException(401, "Invalid user")

        if str(user.password_changed_at) != payload.get("password_changed_at"):
            raise HTTPException(401, "Token invalidated")

        access = create_access_token(user)
        return {"access_token": access}

    def change_password(self, user, schema: ChangePasswordInput):
        if not verify_password(schema.old_password, user.hash_password):
            raise HTTPException(400, "Incorrect old password")

        user.hash_password = hash_password(schema.new_password)
        user.password_changed_at = datetime.utcnow()
        self.db.commit()

        return {"message": "Password updated"}

    def me(self, user):
        return UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            rol=user.rol,
            user_language=user.user_language,
            user_theme=user.user_theme,
            is_active=user.is_active,
            last_login=user.last_login
        ).model_dump()

# src/app/services/auth_service.py
