# file: src/app/repositories/stock_product_location_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.stock_product_location import StockProductLocation

class StockProductLocationRepository(BaseRepository):
    model = StockProductLocation

    def get_by_product_location(self, product_id: int, location_id: int):
        return (
            self.db.query(StockProductLocation)
            .filter(
                StockProductLocation.product_id == product_id,
                StockProductLocation.location_id == location_id,
                StockProductLocation.is_active == True
            )
            .first()
        )
