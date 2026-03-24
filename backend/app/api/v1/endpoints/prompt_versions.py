from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, select

from app.api.deps import OptionalUser, SessionDep
from app.models.tables import Prompt, PromptVersion

router = APIRouter(prefix="/prompts", tags=["prompts"])


class VersionIn(BaseModel):
    content: str = Field(..., max_length=200_000)


@router.post("/{prompt_id}/versions")
async def add_version(
    prompt_id: UUID,
    body: VersionIn,
    session: SessionDep,
    user: OptionalUser,
) -> dict[str, str | int]:
    p = await session.get(Prompt, prompt_id)
    if not p:
        raise HTTPException(status_code=404, detail="Prompt not found")
    if user and p.user_id and p.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    n = await session.scalar(
        select(func.max(PromptVersion.version_number)).where(
            PromptVersion.prompt_id == prompt_id
        )
    )
    next_v = int(n or 0) + 1
    vid = uuid4()
    session.add(
        PromptVersion(
            id=vid,
            prompt_id=prompt_id,
            version_number=next_v,
            content=body.content,
        )
    )
    await session.commit()
    return {"id": str(vid), "version_number": next_v}
