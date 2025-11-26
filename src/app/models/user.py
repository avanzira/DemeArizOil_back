# file: src/app/models/user.py

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from app.db.base import Base
from app.core.mixins.audit_mixin import AuditMixin


class User(Base, AuditMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)

    rol: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
    password_changed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_language: Mapped[str] = mapped_column(String(5), default="es")
    user_theme: Mapped[str] = mapped_column(String(10), default="light")

    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

# end file: src/app/models/user.py