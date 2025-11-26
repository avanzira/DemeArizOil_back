# file: src/app/services/purchase_notes_service.py

from datetime import datetime
from fastapi import HTTPException

from src.app.services.base_service import BaseService
from src.app.services.stock_service import StockService
from src.app.services.cash_service import CashService

from src.app.repositories.purchase_note_repository import PurchaseNoteRepository
from src.app.repositories.line_purchase_note_repository import LinePurchaseNoteRepository
from src.app.repositories.product_repository import ProductRepository
from src.app.repositories.supplier_repository import SupplierRepository
from src.app.repositories.stock_product_location_repository import StockProductLocationRepository

from src.app.schemas.purchase_note_schemas import PurchaseNoteCreate
from src.app.core.config.settings import settings
from src.app.core.enums.stock_enums import StockMoveType

CENTRAL_ID = settings.CENTRAL_STOCK_LOCATION_ID


class PurchaseNotesService(BaseService):
    repo_class = PurchaseNoteRepository

    def __init__(self, db=None):
        super().__init__(db)
        self.lines = LinePurchaseNoteRepository(self.db)
        self.products = ProductRepository(self.db)
        self.suppliers = SupplierRepository(self.db)
        self.stock_rows = StockProductLocationRepository(self.db)
        self.stock_service = StockService(self.db)
        self.cash_service = CashService(self.db)

    def create(self, schema: PurchaseNoteCreate):
        supplier = self.suppliers.get(schema.supplier_id)
        if not supplier:
            raise HTTPException(404, "Supplier not found")
        if not supplier.is_active:
            raise HTTPException(400, "Supplier inactive")

        total = 0
        total_inventory_qty = 0
        inventory_cost = 0

        if not schema.lines:
            raise HTTPException(400, "Purchase must include lines")

        for line in schema.lines:
            product = self.products.get(line.product_id)
            if not product:
                raise HTTPException(404, f"Product {line.product_id} not found")

            if line.quantity <= 0 or line.quantity != int(line.quantity):
                raise HTTPException(400, "Quantity must be positive integer")

            subtotal = float(line.unit_price) * line.quantity
            total += subtotal

            if product.is_inventory:
                total_inventory_qty += line.quantity
                inventory_cost += subtotal

        paid = float(schema.paid)
        if paid < 0 or paid > total:
            raise HTTPException(400, "Invalid paid amount")

        pending = total - paid

        purchase = super().create({
            "supplier_id": schema.supplier_id,
            "account_id": schema.account_id,
            "date": datetime.utcnow(),
            "total": total,
            "paid": paid,
            "pending": pending,
        })

        for line in schema.lines:
            self.lines.create({
                "purchase_id": purchase.id,
                "product_id": line.product_id,
                "quantity": line.quantity,
                "unit_price": float(line.unit_price),
                "line_total": float(line.unit_price) * line.quantity,
            })

        for line in schema.lines:
            product = self.products.get(line.product_id)
            if not product.is_inventory:
                continue

            self.stock_service.register_movement(
                product_id=product.id,
                qty=line.quantity,
                location_from_id=None,
                location_to_id=CENTRAL_ID,
                movement_type=StockMoveType.PURCHASE,
                purchase_id=purchase.id
            )

        if total_inventory_qty > 0:
            for line in schema.lines:
                prod = self.products.get(line.product_id)
                if not prod.is_inventory:
                    continue

                rows = self.db.query(self.stock_rows.model).filter_by(product_id=prod.id).all()
                old_stock = sum(r.quantity for r in rows) - line.quantity
                old_avg = float(prod.cost_average)
                new_stock = old_stock + line.quantity

                if new_stock > 0:
                    new_avg = (old_avg * old_stock + float(line.unit_price) * line.quantity) / new_stock
                else:
                    new_avg = float(line.unit_price)

                prod.cost_average = new_avg

            self.db.commit()

        if paid > 0:
            self.cash_service.register_movement(
                account_from_id=schema.account_id,
                account_to_id=None,
                amount=paid,
                purchase_id=purchase.id
            )

        return purchase

    def pay_debt(self, purchase_id: int, *, account_id: int, amount: float):
        purchase = self._get_or_404(purchase_id)

        if amount <= 0:
            raise HTTPException(400, "Amount must be > 0")

        if amount > purchase.pending:
            raise HTTPException(400, "Amount exceeds pending debt")

        self.cash_service.register_movement(
            account_from_id=account_id,
            account_to_id=None,
            amount=amount,
            purchase_id=purchase.id
        )

        purchase.pending -= amount
        purchase.paid += amount
        self.db.commit()

        return purchase
