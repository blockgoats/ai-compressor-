import uuid
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException
from sqlalchemy import select

from app.api.deps import SessionDep
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.tables import User
from app.schemas.auth import TokenResponse, UserCreate, UserLogin, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register(body: UserCreate, session: SessionDep) -> TokenResponse:
    exists = await session.scalar(select(User).where(User.email == body.email))
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    u = User(
        id=uuid.uuid4(),
        email=body.email,
        hashed_password=get_password_hash(body.password),
    )
    session.add(u)
    await session.commit()
    await session.refresh(u)
    token = create_access_token({"sub": str(u.id)})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLogin, session: SessionDep) -> TokenResponse:
    u = await session.scalar(select(User).where(User.email == body.email))
    if not u or not verify_password(body.password, u.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(u.id)})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserOut)
async def me(
    session: SessionDep,
    authorization: str | None = Header(None, alias="Authorization"),
) -> UserOut:
    from app.core.security import decode_token

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    payload = decode_token(authorization.removeprefix("Bearer ").strip())
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    u = await session.get(User, UUID(payload["sub"]))
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(id=str(u.id), email=u.email)
