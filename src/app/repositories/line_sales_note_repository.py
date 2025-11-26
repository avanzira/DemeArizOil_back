# file: src/app/repositories/line_sales_note_repository.py

from src.app.models.line_sales_note import LineSalesNote


class LineSalesNoteRepository:
    """
    Repositorio simple para líneas de sales_notes.
    Misma estructura que LinePurchaseNoteRepository.
    """

    def __init__(self, db):
        self.db = db
        self.model = LineSalesNote

    def create(self, obj_data: dict):
        obj = self.model(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
