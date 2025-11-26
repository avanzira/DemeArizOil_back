# file: src/app/services/products_service.py
from fastapi import HTTPException

from src.app.services.base_service import BaseService
from src.app.repositories.product_repository import ProductRepository
from src.app.repositories.stock_product_location_repository import StockProductLocationRepository
from src.app.schemas.product_schemas import ProductCreate, ProductUpdate

class ProductsService(BaseService):
    repo_class = ProductRepository

    def __init__(self, db=None):
        super().__init__(db)
        self.stock_rows = StockProductLocationRepository(self.db)

    def create(self, schema: ProductCreate):
        name = schema.name.strip()
        if not name:
            raise HTTPException(400, "Product name cannot be empty")

        if self.db.query(self.repo.model).filter_by(name=name).first():
            raise HTTPException(400, "Product already exists")

        product = super().create({
            "name": name,
            "unit_measure": schema.unit_measure,
            "is_inventory": schema.is_inventory,
            "cost_average": 0
        })

        return product

    def update(self, id: int, schema: ProductUpdate):
        product = self._get_or_404(id)
        updates = {}

        if schema.name is not None:
            nm = schema.name.strip()
            if not nm:
                raise HTTPException(400, "Product name cannot be empty")
            updates["name"] = nm

        if schema.unit_measure is not None:
            updates["unit_measure"] = schema.unit_measure

        if schema.is_inventory is not None:
            rows = self.db.query(self.stock_rows.model).filter_by(product_id=id).all()
            stock_total = sum(r.quantity for r in rows)
            if stock_total > 0 and schema.is_inventory != product.is_inventory:
                raise HTTPException(400, "Cannot change is_inventory for product with stock")
            updates["is_inventory"] = schema.is_inventory

        updated = self.repo.update(product, updates)
        return updated

    def delete(self, id: int):
        product = self._get_or_404(id)
        rows = self.db.query(self.stock_rows.model).filter_by(product_id=id).all()
        stock_total = sum(r.quantity for r in rows)

        if stock_total > 0:
            raise HTTPException(400, "Cannot delete product with stock")

        super().delete(id)
        return {"id": product.id, "deleted": true}