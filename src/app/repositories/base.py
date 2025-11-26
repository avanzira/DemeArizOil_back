# file: src/app/repositories/base.py
from sqlalchemy.orm import Session

class BaseRepository:
    model = None

    def __init__(self, db: Session):
        self.db = db

    def get(self, id: int):
        return (
            self.db.query(self.model)
            .filter(self.model.id == id, self.model.is_active == True)
            .first()
        )

    def get_raw(self, id: int):
        return self.db.get(self.model, id)

    def list(self):
        return self.db.query(self.model).filter(self.model.is_active == True).all()

    def create(self, obj_data: dict):
        obj = self.model(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj, data: dict):
        for k, v in data.items():
            if v is not None:
                setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj):
        obj.is_active = False
        self.db.commit()
        return obj
