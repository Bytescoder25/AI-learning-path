"""Schemas for similarity search."""
import uuid

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)


class Citation(BaseModel):
    chunk_id: uuid.UUID
    document_id: uuid.UUID
    source: str
    content: str
    score: float = Field(..., description="Similarity score (higher = closer).")


class SearchResponse(BaseModel):
    query: str
    results: list[Citation]
