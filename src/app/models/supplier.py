# file: src/app/models/supplier.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from src.app.db.base import Base
from src.app.core.mixins.audit_mixin import AuditMixin


class Supplier(Base, AuditMixin):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(100))
    address: Mapped[str | None] = mapped_column(String(200))

    purchases = relationship("PurchaseNote", back_populates="supplier")

# end file: src/app/models/supplier.py