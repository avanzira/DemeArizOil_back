# file: src/app/services/base_service.py

from typing import Type
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.app.core.config.database import get_session
from src.app.repositories.base import BaseRepository


class BaseService:
    repo_class: Type[BaseRepository] = None

    def __init__(self, db: Session | None = None):
        self.db = db or get_session()
        if not self.repo_class:
            raise RuntimeError("repo_class not defined in service")
        self.repo = self.repo_class(self.db)

    def _get_or_404(self, id: int):
        obj = self.repo.get(id)
        if not obj:
            raise HTTPException(404, "Object not found")
        return obj

    def list(self):
        return self.repo.list()

    def get(self, id: int):
        return self._get_or_404(id)

    def create(self, data: dict):
        return self.repo.create(data)

    def update(self, id: int, data: dict):
        obj = self._get_or_404(id)
        return self.repo.update(obj, data)

    def delete(self, id: int):
        obj = self._get_or_404(id)
        return self.repo.delete(obj)
