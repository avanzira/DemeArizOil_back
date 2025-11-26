# file: src/app/models/product.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Numeric
from src.app.db.base import Base
from src.app.core.mixins.audit_mixin import AuditMixin


class Product(Base, AuditMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    unit_measure: Mapped[str] = mapped_column(String(20), nullable=False)
    is_inventory: Mapped[bool] = mapped_column(Boolean, nullable=False)

    cost_average: Mapped[float] = mapped_column(Numeric(18,4), default=0)

    purchase_lines = relationship("LinePurchaseNote", back_populates="product")
    sales_lines = relationship("LineSalesNote", back_populates="product")
    stock_rows = relationship("StockProductLocation", back_populates="product")
    stock_movements = relationship("StockMovement", back_populates="product")

# end file: src/app/models/product.py