# file: src/app/models/stock_movement.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, String
from datetime import datetime
from app.db.base import Base
from app.core.enums.stock_enums import StockMoveType
from app.core.mixins.audit_mixin import AuditMixin


class StockMovement(Base, AuditMixin):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    location_from_id: Mapped[int | None] = mapped_column(ForeignKey("stock_locations.id"))
    location_to_id: Mapped[int | None] = mapped_column(ForeignKey("stock_locations.id"))

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[StockMoveType] = mapped_column(String(20), nullable=False)

    purchase_id: Mapped[int | None] = mapped_column(ForeignKey("purchase_notes.id"))
    sales_id: Mapped[int | None] = mapped_column(ForeignKey("sales_notes.id"))

    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="stock_movements")
    location_from = relationship("StockLocation", foreign_keys=[location_from_id], back_populates="moves_from")
    location_to = relationship("StockLocation", foreign_keys=[location_to_id], back_populates="moves_to")

    purchase = relationship("PurchaseNote", back_populates="stock_movements")
    sales = relationship("SalesNote", back_populates="stock_movements")

# end file: src/app/models/stock_movement.py