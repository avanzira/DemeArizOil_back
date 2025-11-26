# file: src/app/models/cash_movement.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base
from app.core.mixins.audit_mixin import AuditMixin


class CashMovement(Base, AuditMixin):
    __tablename__ = "cash_movements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_from_id: Mapped[int | None] = mapped_column(ForeignKey("cash_accounts.id"))
    account_to_id: Mapped[int | None] = mapped_column(ForeignKey("cash_accounts.id"))
    amount: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    purchase_id: Mapped[int | None] = mapped_column(ForeignKey("purchase_notes.id"))
    sales_id: Mapped[int | None] = mapped_column(ForeignKey("sales_notes.id"))

    account_from = relationship("CashAccount", foreign_keys=[account_from_id], back_populates="movements_from")
    account_to = relationship("CashAccount", foreign_keys=[account_to_id], back_populates="movements_to")

    purchase = relationship("PurchaseNote", back_populates="cash_movements")
    sales = relationship("SalesNote", back_populates="cash_movements")

# end file: src/app/models/cash_movement.py