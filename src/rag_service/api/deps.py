"""Shared FastAPI dependencies (auth). DB session dependency lives in db.session."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from rag_service.core.security import decode_access_token

_bearer = HTTPBearer(auto_error=False)


async def get_current_subject(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> str:
    """Verify the JWT and return its subject. Reuse on any protected route."""
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")
    subject = decode_access_token(credentials.credentials)
    if subject is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    return subject
