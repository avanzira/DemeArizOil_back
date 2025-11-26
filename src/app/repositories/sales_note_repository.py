# file: src/app/repositories/sales_note_repository.py
from app.repositories.base import BaseRepository
from app.models.sales_note import SalesNote

class SalesNoteRepository(BaseRepository):
    model = SalesNote
