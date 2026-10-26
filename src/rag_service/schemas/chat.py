"""Schemas for RAG chat."""
from pydantic import BaseModel, Field

from rag_service.schemas.search import Citation


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: str | None = None
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    """Non-streaming shape. The /chat route streams tokens; this documents the
    full assembled result (answer + which chunks grounded it)."""
    answer: str
    citations: list[Citation]
