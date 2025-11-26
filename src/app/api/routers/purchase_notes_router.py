# file: src/app/api/routers/purchase_notes_router.py

from fastapi import APIRouter, Depends
from src.app.schemas.purchase_note_schemas import PurchaseNoteCreate, PurchaseNoteOut
from src.app.services.purchase_notes_service import PurchaseNotesService
from sqlalchemy.orm import Session
from src.app.security.jwt import get_current_user
from src.app.core.config.deps import get_db

router = APIRouter(prefix="/purchase-notes", tags=["purchase-notes"])

@router.post("/", response_model=PurchaseNoteOut)
def create_purchase_note(data: PurchaseNoteCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return PurchaseNotesService(db).create(data)

@router.get("/", response_model=list[PurchaseNoteOut])
def list_purchase_notes(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return PurchaseNotesService(db).list()
