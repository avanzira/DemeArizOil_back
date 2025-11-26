# file: src/app/core/config/settings.py

import os
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "DemeArizOil"
    DEBUG: bool = True

    # Campos individuales para construir la URL en local
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_host: Optional[str] = None
    db_name: Optional[str] = None

    # URL completa (Railway la inyecta como DATABASE_URL)
    DATABASE_URL: Optional[str] = None

    SECRET_KEY: str = Field(..., description="JWT signing key")

    CORS_ORIGINS: List[str] = ["*"]

    CENTRAL_STOCK_LOCATION_ID: int = 1

    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def model_post_init(self, __context) -> None:
        # 1) Si ya viene DATABASE_URL (Railway), se respeta
        if not self.DATABASE_URL:
            # 2) Compatibilidad con RAILWAY_DATABASE_URL si existiera
            railway_url = os.getenv("RAILWAY_DATABASE_URL")
            if railway_url:
                self.DATABASE_URL = railway_url
            # 3) Construcción a partir de db_* (entorno local / docker-compose)
            elif self.db_user and self.db_password and self.db_host and self.db_name:
                self.DATABASE_URL = (
                    f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
                    f"@{self.db_host}:5432/{self.db_name}"
                )

        # Bloquear arranque sin URL de base de datos
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not configured.")


settings = Settings()

# end file: src/app/core/config/settings.py
