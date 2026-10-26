"""Streaming RAG chat endpoint.

Streams the answer token-by-token via Server-Sent Events, and sends the
citations first as a `meta` event so the client can render sources immediately.
"""
import json
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from rag_service.api.deps import get_current_subject
from rag_service.db.session import get_session
from rag_service.rag.pipeline import answer_question
from rag_service.schemas.chat import ChatRequest

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat(
    body: ChatRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
    _: Annotated[str, Depends(get_current_subject)],
) -> StreamingResponse:
    history = [m.model_dump() for m in body.history]
    token_stream, citations = await answer_question(session, body.message, history)

    async def event_generator():
        meta = {"citations": [c.model_dump(mode="json") for c in citations]}
        yield f"event: meta\ndata: {json.dumps(meta)}\n\n"
        async for delta in token_stream:
            yield f"event: token\ndata: {json.dumps({'text': delta})}\n\n"
        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
