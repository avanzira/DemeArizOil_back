# file: src/app/repositories/stock_movement_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.stock_movement import StockMovement

class StockMovementRepository(BaseRepository):
    model = StockMovement
