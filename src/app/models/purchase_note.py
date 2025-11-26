# file: src/app/models/purchase_note.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, DateTime, ForeignKey
from datetime import datetime
from src.app.db.base import Base
from src.app.core.mixins.audit_mixin import AuditMixin


class PurchaseNote(Base, AuditMixin):
    __tablename__ = "purchase_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    account_id: Mapped[int | None] = mapped_column(ForeignKey("cash_accounts.id"))

    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    total: Mapped[float] = mapped_column(Numeric(18,2), default=0)
    paid: Mapped[float] = mapped_column(Numeric(18,2), default=0)
    pending: Mapped[float] = mapped_column(Numeric(18,2), default=0)

    supplier = relationship("Supplier", back_populates="purchases")
    account = relationship("CashAccount")

    lines = relationship("LinePurchaseNote", back_populates="purchase")
    stock_movements = relationship("StockMovement", back_populates="purchase")
    cash_movements = relationship("CashMovement", back_populates="purchase")

# end file: src/app/models/purchase_note.py