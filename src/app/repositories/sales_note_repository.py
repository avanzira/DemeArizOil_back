# file: src/app/repositories/sales_note_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.sales_note import SalesNote

class SalesNoteRepository(BaseRepository):
    model = SalesNote
