from fastapi import FastAPI

from app.core.config import settings
from app.api.routers import api_router

app = FastAPI(title=settings.app_title)

app.include_router(api_router)
