# file: src/app/repositories/purchase_note_repository.py
from app.repositories.base import BaseRepository
from app.models.purchase_note import PurchaseNote

class PurchaseNoteRepository(BaseRepository):
    model = PurchaseNote
