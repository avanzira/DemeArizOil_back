# file: src/app/repositories/purchase_note_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.purchase_note import PurchaseNote

class PurchaseNoteRepository(BaseRepository):
    model = PurchaseNote
