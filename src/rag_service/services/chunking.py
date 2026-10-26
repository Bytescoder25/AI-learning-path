"""Chunking — split a document into overlapping windows before embedding.

Week 2 starts with the simplest strategy (fixed-size + overlap). You'll swap in
sentence/structure-aware chunking in Month 5 (advanced RAG). Keeping this behind
one function means the rest of the pipeline never changes when you do.
"""
from rag_service.config import get_settings


def chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> list[str]:
    """Fixed-size character chunking with overlap.

    Trade-off to remember: too small loses context, too big dilutes relevance.
    """
    settings = get_settings()
    size = chunk_size or settings.chunk_size
    step = size - (overlap if overlap is not None else settings.chunk_overlap)
    if step <= 0:
        raise ValueError("overlap must be smaller than chunk_size")

    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    for start in range(0, len(text), step):
        piece = text[start : start + size].strip()
        if piece:
            chunks.append(piece)
    return chunks
