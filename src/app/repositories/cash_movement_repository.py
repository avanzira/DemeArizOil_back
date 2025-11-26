# file: src/app/repositories/cash_movement_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.cash_movement import CashMovement

class CashMovementRepository(BaseRepository):
    model = CashMovement
