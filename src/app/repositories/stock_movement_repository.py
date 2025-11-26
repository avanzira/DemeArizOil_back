# file: src/app/repositories/stock_movement_repository.py
from app.repositories.base import BaseRepository
from app.models.stock_movement import StockMovement

class StockMovementRepository(BaseRepository):
    model = StockMovement
