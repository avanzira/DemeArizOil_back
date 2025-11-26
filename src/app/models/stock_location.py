# file: src/app/models/stock_location.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from app.db.base import Base
from app.core.enums.stock_enums import StockLocationType
from app.core.mixins.audit_mixin import AuditMixin


class StockLocation(Base, AuditMixin):
    __tablename__ = "stock_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[StockLocationType] = mapped_column(String(20), nullable=False)

    stock_rows = relationship("StockProductLocation", back_populates="location")

    moves_from = relationship(
        "StockMovement",
        foreign_keys="StockMovement.location_from_id",
        back_populates="location_from"
    )
    moves_to = relationship(
        "StockMovement",
        foreign_keys="StockMovement.location_to_id",
        back_populates="location_to"
    )

# end file: src/app/models/stock_location.py