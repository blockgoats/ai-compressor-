from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import decode_token
from app.db.session import get_session
from app.models.tables import User

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_optional_user(
    session: SessionDep,
    authorization: str | None = Header(None, alias="Authorization"),
) -> User | None:
    settings = get_settings()
    if settings.auth_disable:
        return None
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.removeprefix("Bearer ").strip()
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        return None
    uid = payload["sub"]
    from uuid import UUID

    try:
        u = await session.get(User, UUID(uid))
    except Exception:
        return None
    return u


OptionalUser = Annotated[User | None, Depends(get_optional_user)]
