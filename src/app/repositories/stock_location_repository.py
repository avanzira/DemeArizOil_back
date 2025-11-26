# file: src/app/repositories/stock_location_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.stock_location import StockLocation

class StockLocationRepository(BaseRepository):
    model = StockLocation
