"""Document ingestion + listing endpoints."""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from rag_service.api.deps import get_current_subject
from rag_service.db.models import Document
from rag_service.db.session import get_session
from rag_service.schemas.document import DocumentCreate, DocumentOut
from rag_service.services.ingestion import ingest_document

router = APIRouter(prefix="/documents", tags=["documents"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]
AuthDep = Annotated[str, Depends(get_current_subject)]


def _to_out(doc: Document) -> DocumentOut:
    return DocumentOut(
        id=doc.id,
        source=doc.source,
        meta=doc.meta,
        chunk_count=len(doc.chunks),
        created_at=doc.created_at,
    )


@router.post("", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def create_document(body: DocumentCreate, session: SessionDep, _: AuthDep) -> DocumentOut:
    doc = await ingest_document(session, body.source, body.content, body.meta)
    await session.flush()
    return _to_out(doc)


@router.get("", response_model=list[DocumentOut])
async def list_documents(session: SessionDep, _: AuthDep) -> list[DocumentOut]:
    stmt = select(Document).options(selectinload(Document.chunks)).order_by(Document.created_at.desc())
    docs = (await session.execute(stmt)).scalars().all()
    return [_to_out(d) for d in docs]


@router.get("/{document_id}", response_model=DocumentOut)
async def get_document(document_id: uuid.UUID, session: SessionDep, _: AuthDep) -> DocumentOut:
    stmt = select(Document).options(selectinload(Document.chunks)).where(Document.id == document_id)
    doc = (await session.execute(stmt)).scalar_one_or_none()
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    return _to_out(doc)
