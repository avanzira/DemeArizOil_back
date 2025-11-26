# file: src/app/repositories/cash_account_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.cash_account import CashAccount

class CashAccountRepository(BaseRepository):
    model = CashAccount
