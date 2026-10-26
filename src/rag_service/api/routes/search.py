"""Similarity search endpoint — retrieval without generation."""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rag_service.api.deps import get_current_subject
from rag_service.db.session import get_session
from rag_service.schemas.search import SearchRequest, SearchResponse
from rag_service.services.retrieval import similarity_search

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
async def search(
    body: SearchRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    _: Annotated[str, Depends(get_current_subject)],
) -> SearchResponse:
    results = await similarity_search(session, body.query, top_k=body.top_k)
    return SearchResponse(query=body.query, results=results)
