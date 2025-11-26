# file: src/app/security/middleware.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.app.core.config.settings import settings

# Global middleware placeholder
def apply_middlewares(app: FastAPI):
    @app.middleware("http")
    async def security_middleware(request: Request, call_next):
        response = await call_next(request)
        return response

    return app
