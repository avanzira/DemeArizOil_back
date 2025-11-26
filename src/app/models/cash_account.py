# file: src/app/models/cash_account.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from src.app.db.base import Base
from src.app.core.mixins.audit_mixin import AuditMixin


class CashAccount(Base, AuditMixin):
    __tablename__ = "cash_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    movements_from = relationship(
        "CashMovement",
        foreign_keys="CashMovement.account_from_id",
        back_populates="account_from"
    )
    movements_to = relationship(
        "CashMovement",
        foreign_keys="CashMovement.account_to_id",
        back_populates="account_to"
    )

# end file: src/app/models/cash_account.py