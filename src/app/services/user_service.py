# file: src/app/services/user_service.py

from datetime import datetime
from fastapi import HTTPException

from app.services.base_service import BaseService
from app.repositories.user_repository import UserRepository
from app.security.password import hash_password, verify_password
from app.schemas.user_schemas import (
    UserCreate,
    UserUpdate,
    ChangePasswordAdmin,
    UpdatePreferences,
)


class UserService(BaseService):
    repo_class = UserRepository

    def __init__(self, db=None):
        super().__init__(db)

    def _admin_required(self, current_user):
        if current_user.rol != "admin":
            raise HTTPException(403, "Admin only")

    def list(self, current_user):
        self._admin_required(current_user)
        return super().list()

    def create(self, schema: UserCreate, current_user):
        self._admin_required(current_user)

        username = schema.username.strip()
        email = schema.email.strip().lower()

        if self.repo.get_by_username(username):
            raise HTTPException(400, "Username already exists")

        if self.repo.get_by_email(email):
            raise HTTPException(400, "Email already exists")

        hashed = hash_password(schema.password)

        return super().create({
            "username": username,
            "email": email,
            "hash_password": hashed,
            "rol": schema.rol,
            "user_language": "es",
            "user_theme": "light",
            "password_changed_at": datetime.utcnow()
        })

    def update(self, id: int, schema: UserUpdate, current_user):
        self._admin_required(current_user)
        user = self._get_or_404(id)

        updates = {}

        if schema.username is not None:
            nm = schema.username.strip()
            if nm != user.username:
                if self.repo.get_by_username(nm):
                    raise HTTPException(400, "Username already exists")
            updates["username"] = nm

        if schema.email is not None:
            mail = schema.email.strip().lower()
            if mail != user.email:
                if self.repo.get_by_email(mail):
                    raise HTTPException(400, "Email already exists")
            updates["email"] = mail

        if schema.rol is not None:
            updates["rol"] = schema.rol

        if schema.user_language is not None:
            updates["user_language"] = schema.user_language
        if schema.user_theme is not None:
            updates["user_theme"] = schema.user_theme

        return self.repo.update(user, updates)

    def delete(self, id: int, current_user):
        self._admin_required(current_user)
        return super().delete(id)

    def change_password_admin(self, id: int, schema: ChangePasswordAdmin, current_user):
        self._admin_required(current_user)
        user = self._get_or_404(id)

        new_hash = hash_password(schema.new_password)

        return self.repo.update(user, {
            "hash_password": new_hash,
            "password_changed_at": datetime.utcnow()
        })

    def update_preferences(self, id: int, schema: UpdatePreferences):
        user = self._get_or_404(id)

        updates = {}
        if schema.user_language is not None:
            updates["user_language"] = schema.user_language
        if schema.user_theme is not None:
            updates["user_theme"] = schema.user_theme

        return self.repo.update(user, updates)
