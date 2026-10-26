"""FastAPI application entrypoint.

Run locally:  uvicorn rag_service.main:app --reload
Docs:         http://localhost:8000/docs
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from rag_service.api.routes import chat, documents, health, search
from rag_service.config import get_settings
from rag_service.core.logging import configure_logging, get_logger

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    get_logger().info("startup", app=settings.app_name, env=settings.environment)
    yield
    get_logger().info("shutdown")


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.include_router(health.router)
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(chat.router)
