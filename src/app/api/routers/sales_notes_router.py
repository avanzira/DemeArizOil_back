# file: src/app/api/routers/sales_notes_router.py
# Nota: funciones sueltas por recomendación FastAPI.

from fastapi import APIRouter, Depends
from app.services.sales_notes_service import SalesNotesService
from app.schemas.sales_note_schemas import SalesNoteCreate
from app.security.jwt import get_current_user

router = APIRouter(prefix="/sales-notes", tags=["sales_notes"])

@router.get("/")
def list_sales_notes(user = Depends(get_current_user)):
    return SalesNotesService().list()

@router.post("/")
def create_sales_note(data: SalesNoteCreate, user = Depends(get_current_user)):
    return SalesNotesService().create(data)
