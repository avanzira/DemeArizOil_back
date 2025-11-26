# file: src/app/main.py
from fastapi import FastAPI

from app.api.api_router import api_router
from app.security.middleware import apply_middlewares
from app.security.cors import apply_cors
from app.core.exceptions.handlers import register_exception_handlers
from app.core.config.settings import settings


# Create application
app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Load middlewares
apply_middlewares(app)
apply_cors(app)
register_exception_handlers(app)

# Load API routers
app.include_router(api_router)


@app.get("/")
def root():
    return {"app": settings.APP_NAME, "status": "ok"}
