"""Retrieval — the read path: query -> embed -> pgvector nearest-neighbor search.

Uses cosine distance (`<=>`). Score is 1 - distance so higher = more similar.
This is the heart of RAG retrieval; hybrid search + re-ranking get layered on
top of this in Month 5.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rag_service.db.models import Chunk, Document
from rag_service.schemas.search import Citation
from rag_service.services.embeddings import embed_query


async def similarity_search(
    session: AsyncSession, query: str, top_k: int = 5
) -> list[Citation]:
    query_vector = await embed_query(query)

    distance = Chunk.embedding.cosine_distance(query_vector).label("distance")
    stmt = (
        select(Chunk, Document.source, distance)
        .join(Document, Chunk.document_id == Document.id)
        .order_by(distance)
        .limit(top_k)
    )
    rows = (await session.execute(stmt)).all()

    return [
        Citation(
            chunk_id=chunk.id,
            document_id=chunk.document_id,
            source=source,
            content=chunk.content,
            score=1.0 - float(dist),
        )
        for chunk, source, dist in rows
    ]
