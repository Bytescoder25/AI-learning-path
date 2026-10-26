"""Ingestion — the write path: text -> chunks -> embeddings -> Postgres.

Ties chunking + embeddings + persistence together in one transaction.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from rag_service.db.models import Chunk, Document
from rag_service.services.chunking import chunk_text
from rag_service.services.embeddings import embed_texts


async def ingest_document(
    session: AsyncSession, source: str, content: str, meta: dict | None = None
) -> Document:
    """Chunk, embed, and store a document. Returns the persisted Document."""
    pieces = chunk_text(content)
    vectors = await embed_texts(pieces)

    document = Document(source=source, meta=meta or {})
    document.chunks = [
        Chunk(chunk_index=i, content=piece, embedding=vector)
        for i, (piece, vector) in enumerate(zip(pieces, vectors, strict=True))
    ]
    session.add(document)
    await session.flush()  # populate document.id without ending the transaction
    return document
