# file: src/app/repositories/stock_location_repository.py
from app.repositories.base import BaseRepository
from app.models.stock_location import StockLocation

class StockLocationRepository(BaseRepository):
    model = StockLocation
