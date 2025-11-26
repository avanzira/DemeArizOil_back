# file: src/app/core/config/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.app.core.config.settings import settings


_engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

_SessionLocal = sessionmaker(
    bind=_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)


def get_session() -> Session:
    return _SessionLocal()


# end file: src/app/core/config/database.py
