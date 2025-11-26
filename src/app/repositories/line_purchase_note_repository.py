# file: src/app/repositories/line_purchase_note_repository.py

from app.models.line_purchase_note import LinePurchaseNote


class LinePurchaseNoteRepository:
    """
    Repositorio simple para líneas de purchase_notes.
    No hereda de BaseRepository porque no necesita list/get/update/delete.
    Solo create, igual que en tus repos originales.
    """

    def __init__(self, db):
        self.db = db
        self.model = LinePurchaseNote

    def create(self, obj_data: dict):
        obj = self.model(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
