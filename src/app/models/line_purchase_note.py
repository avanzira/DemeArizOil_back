# file: src/app/models/line_purchase_note.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, ForeignKey
from src.app.db.base import Base
from src.app.core.mixins.audit_mixin import AuditMixin


class LinePurchaseNote(Base, AuditMixin):
    __tablename__ = "line_purchase_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchase_notes.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18,3), nullable=False)
    line_total: Mapped[float] = mapped_column(Numeric(18,2), nullable=False)

    product = relationship("Product", back_populates="purchase_lines")
    purchase = relationship("PurchaseNote", back_populates="lines")

# end file: src/app/models/line_purchase_note.py