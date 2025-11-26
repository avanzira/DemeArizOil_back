# file: src/app/services/stock_service.py

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config.database import get_session
from app.core.enums.stock_enums import StockMoveType
from app.repositories.product_repository import ProductRepository
from app.repositories.stock_location_repository import StockLocationRepository
from app.repositories.stock_product_location_repository import StockProductLocationRepository
from app.repositories.stock_movement_repository import StockMovementRepository


class StockService:
    """
    Servicio especializado para movimientos y consultas de stock.
    Incluye:
        - list_locations()
        - get_stock_by_product()
        - get_stock_total()
        - register_movement()
    """

    def __init__(self, db: Session | None = None):
        self.db = db or get_session()
        self.products = ProductRepository(self.db)
        self.locations = StockLocationRepository(self.db)
        self.rows = StockProductLocationRepository(self.db)
        self.movements = StockMovementRepository(self.db)

    # -----------------------------
    # NUEVO → lista de ubicaciones
    # -----------------------------
    def list_locations(self):
        return self.locations.list()

    # -----------------------------
    # NUEVO → stock detallado por producto
    # -----------------------------
    def get_stock_by_product(self, product_id: int):
        product = self.products.get(product_id)
        if not product:
            raise HTTPException(404, "Product not found")

        rows = (
            self.db.query(self.rows.model)
            .filter_by(product_id=product_id)
            .all()
        )

        per_location = []
        total_qty = 0

        for r in rows:
            loc = self.locations.get(r.location_id)
            per_location.append({
                "location_id": loc.id,
                "location_name": loc.name,
                "quantity": r.quantity
            })
            total_qty += r.quantity

        return {
            "product_id": product.id,
            "product_name": product.name,
            "stock_total": total_qty,
            "per_location": per_location
        }

    # -----------------------------
    # NUEVO → total por producto
    # -----------------------------
    def get_stock_total(self, product_id: int):
        product = self.products.get(product_id)
        if not product:
            raise HTTPException(404, "Product not found")

        rows = (
            self.db.query(self.rows.model)
            .filter_by(product_id=product_id)
            .all()
        )

        return sum(r.quantity for r in rows)

    # -----------------------------
    # Movimiento atómico
    # -----------------------------
    def register_movement(
        self,
        *,
        product_id: int,
        qty: int,
        location_from_id: int | None,
        location_to_id: int | None,
        movement_type: StockMoveType,
        purchase_id: int | None = None,
        sales_id: int | None = None,
    ):
        if qty <= 0 or qty != int(qty):
            raise HTTPException(400, "Quantity must be positive integer")

        # validar producto
        if not self.products.get(product_id):
            raise HTTPException(404, "Product not found")

        # validar locations
        if location_from_id is not None and not self.locations.get(location_from_id):
            raise HTTPException(404, "Origin location not found")

        if location_to_id is not None and not self.locations.get(location_to_id):
            raise HTTPException(404, "Destination location not found")

        # ORIGEN
        if location_from_id is not None:
            row_from = self.rows.get_by_product_location(product_id, location_from_id)
            if not row_from or row_from.quantity < qty:
                raise HTTPException(400, "Insufficient stock in origin location")
            row_from.quantity -= qty

        # DESTINO
        if location_to_id is not None:
            row_to = self.rows.get_by_product_location(product_id, location_to_id)
            if not row_to:
                row_to = self.rows.create({
                    "product_id": product_id,
                    "location_id": location_to_id,
                    "quantity": 0
                })
            row_to.quantity += qty

        # registrar movimiento
        self.movements.create({
            "product_id": product_id,
            "location_from_id": location_from_id,
            "location_to_id": location_to_id,
            "quantity": qty,
            "type": movement_type,
            "purchase_id": purchase_id,
            "sales_id": sales_id
        })

        self.db.commit()
        return True
