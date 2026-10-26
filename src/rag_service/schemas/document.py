"""Request/response schemas for document ingestion (the API contract)."""
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    source: str = Field(..., description="Where this doc came from (filename, URL, title).")
    content: str = Field(..., min_length=1, description="Raw text to chunk + embed.")
    meta: dict = Field(default_factory=dict)


class DocumentOut(BaseModel):
    id: uuid.UUID
    source: str
    meta: dict
    chunk_count: int
    created_at: datetime

    model_config = {"from_attributes": True}
