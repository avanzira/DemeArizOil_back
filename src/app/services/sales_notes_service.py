# file: src/app/services/sales_notes_service.py

from datetime import datetime
from fastapi import HTTPException

from app.services.base_service import BaseService
from app.services.stock_service import StockService
from app.services.cash_service import CashService

from app.repositories.sales_note_repository import SalesNoteRepository
from app.repositories.line_sales_note_repository import LineSalesNoteRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.stock_product_location_repository import StockProductLocationRepository
from app.repositories.stock_location_repository import StockLocationRepository

from app.schemas.sales_note_schemas import SalesNoteCreate
from app.core.enums.stock_enums import StockMoveType
from app.core.config.settings import settings

CENTRAL_ID = settings.CENTRAL_STOCK_LOCATION_ID


class SalesNotesService(BaseService):
    repo_class = SalesNoteRepository

    def __init__(self, db=None):
        super().__init__(db)
        self.lines = LineSalesNoteRepository(self.db)
        self.customers = CustomerRepository(self.db)
        self.products = ProductRepository(self.db)
        self.rows = StockProductLocationRepository(self.db)
        self.locations = StockLocationRepository(self.db)
        self.stock_service = StockService(self.db)
        self.cash_service = CashService(self.db)

    def _customer_location_id(self, customer_id: int) -> int:
        loc = self.db.query(self.locations.model).filter_by(
            name=f"customer_{customer_id}_stock"
        ).first()

        if not loc:
            raise HTTPException(500, "Customer stock location missing")
        return loc.id

    def _get_row(self, product_id: int, location_id: int):
        return self.rows.get_by_product_location(product_id, location_id)

    def create(self, schema: SalesNoteCreate):
        customer = self.customers.get(schema.customer_id)
        if not customer:
            raise HTTPException(404, "Customer not found")
        if not customer.is_active:
            raise HTTPException(400, "Customer inactive")

        if not schema.lines:
            raise HTTPException(400, "Sale must contain lines")

        total = 0
        for line in schema.lines:
            if line.quantity <= 0 or line.quantity != int(line.quantity):
                raise HTTPException(400, "Quantity must be positive integer")

            product = self.products.get(line.product_id)
            if not product:
                raise HTTPException(404, f"Product {line.product_id} not found")

            total += float(line.unit_price) * line.quantity

        if total <= 0:
            raise HTTPException(400, "Total must be > 0")

        customer_loc_id = self._customer_location_id(schema.customer_id)

        for line in schema.lines:
            product = self.products.get(line.product_id)

            if not product.is_inventory:
                continue

            qty_needed = int(line.quantity)

            row_customer = self._get_row(product.id, customer_loc_id)
            if row_customer:
                take = min(row_customer.quantity, qty_needed)
                if take > 0:
                    row_customer.quantity -= take
                    qty_needed -= take

            if qty_needed > 0:
                row_central = self._get_row(product.id, CENTRAL_ID)
                if not row_central or row_central.quantity < qty_needed:
                    raise HTTPException(400, "Insufficient stock for sale")
                row_central.quantity -= qty_needed
                qty_needed = 0

            self.stock_service.register_movement(
                product_id=product.id,
                qty=line.quantity,
                location_from_id=None,
                location_to_id=None,
                movement_type=StockMoveType.SALE,
                sales_id=None
            )

        self.db.commit()

        sale = super().create({
            "customer_id": schema.customer_id,
            "account_id": schema.account_id,
            "date": datetime.utcnow(),
            "total": total
        })

        for line in schema.lines:
            self.lines.create({
                "sales_id": sale.id,
                "product_id": line.product_id,
                "quantity": int(line.quantity),
                "unit_price": float(line.unit_price),
                "line_total": float(line.unit_price) * int(line.quantity)
            })

        self.cash_service.register_movement(
            account_from_id=schema.account_id,
            account_to_id=None,
            amount=total,
            sales_id=sale.id
        )

        return sale
