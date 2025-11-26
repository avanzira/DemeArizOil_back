# file: src/app/security/cors.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.app.core.config.settings import settings

def apply_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
