# file: src/app/repositories/cash_movement_repository.py
from app.repositories.base import BaseRepository
from app.models.cash_movement import CashMovement

class CashMovementRepository(BaseRepository):
    model = CashMovement
