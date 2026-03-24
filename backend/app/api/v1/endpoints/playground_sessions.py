from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.api.deps import OptionalUser, SessionDep
from app.models.tables import PlaygroundSession

router = APIRouter(prefix="/playground/sessions", tags=["playground"])


class PlaygroundSessionIn(BaseModel):
    original_prompt: str = Field(..., max_length=200_000)
    compressed_prompt: str = ""
    llm_output: str | None = None
    mode: str = "lossy"
    compression_level: str = "medium"
    tokens_before: int = 0
    tokens_after: int = 0
    metrics: dict | None = None


@router.post("")
async def save_session(
    body: PlaygroundSessionIn,
    session: SessionDep,
    user: OptionalUser,
) -> dict[str, str]:
    uid = user.id if user else None
    sid = uuid4()
    session.add(
        PlaygroundSession(
            id=sid,
            user_id=uid,
            original_prompt=body.original_prompt,
            compressed_prompt=body.compressed_prompt,
            llm_output=body.llm_output,
            mode=body.mode,
            compression_level=body.compression_level,
            tokens_before=body.tokens_before,
            tokens_after=body.tokens_after,
            metrics=body.metrics,
        )
    )
    await session.commit()
    return {"id": str(sid)}
