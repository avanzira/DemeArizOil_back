# file: src/app/models/stock_product_location.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from app.db.base import Base
from app.core.mixins.audit_mixin import AuditMixin


class StockProductLocation(Base, AuditMixin):
    __tablename__ = "stock_product_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    location_id: Mapped[int] = mapped_column(ForeignKey("stock_locations.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("product_id", "location_id", name="uq_product_location"),
    )

    product = relationship("Product", back_populates="stock_rows")
    location = relationship("StockLocation", back_populates="stock_rows")

# end file: src/app/models/stock_product_location.py