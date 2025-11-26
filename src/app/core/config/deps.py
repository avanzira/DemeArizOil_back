# file: src/app/core/config/deps.py

from src.app.core.config.database import get_session
from sqlalchemy.orm import Session

def get_db() -> Session:
    db = get_session()
    try:
        yield db
    finally:
        db.close()
