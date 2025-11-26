# file: src/app/models/line_sales_note.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Numeric, ForeignKey
from app.db.base import Base
from app.core.mixins.audit_mixin import AuditMixin


class LineSalesNote(Base, AuditMixin):
    __tablename__ = "line_sales_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sales_id: Mapped[int] = mapped_column(ForeignKey("sales_notes.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(18,3), nullable=False)
    line_total: Mapped[float] = mapped_column(Numeric(18,2), nullable=False)

    product = relationship("Product", back_populates="sales_lines")
    sales = relationship("SalesNote", back_populates="lines")

# end file: src/app/models/line_sales_note.py