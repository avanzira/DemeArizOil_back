# file: src/app/repositories/cash_account_repository.py
from app.repositories.base import BaseRepository
from app.models.cash_account import CashAccount

class CashAccountRepository(BaseRepository):
    model = CashAccount
