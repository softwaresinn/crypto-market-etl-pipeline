from fastapi import FastAPI
from api.router import api_router
from core.config import get_settings
from core.logging import configure_logging

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router)
