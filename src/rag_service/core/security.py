"""JWT auth helpers — mint and verify tokens.

Kept minimal on purpose; wire real user storage in later. Mirrors the Express
JWT middleware pattern you already know.
"""
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from rag_service.config import get_settings


def create_access_token(subject: str) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str | None:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload.get("sub")
    except JWTError:
        return None
