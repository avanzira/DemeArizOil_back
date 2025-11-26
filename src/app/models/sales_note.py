# file: src/app/models/sales_note.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, DateTime, ForeignKey
from datetime import datetime
from src.app.db.base import Base
from src.app.core.mixins.audit_mixin import AuditMixin


class SalesNote(Base, AuditMixin):
    __tablename__ = "sales_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("cash_accounts.id"))

    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total: Mapped[float] = mapped_column(Numeric(18,2), default=0)

    customer = relationship("Customer", back_populates="sales")
    account = relationship("CashAccount")

    lines = relationship("LineSalesNote", back_populates="sales")
    stock_movements = relationship("StockMovement", back_populates="sales")
    cash_movements = relationship("CashMovement", back_populates="sales")

# end file: src/app/models/sales_note.py