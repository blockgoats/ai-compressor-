from uuid import uuid4

from fastapi import APIRouter

from app.api.deps import OptionalUser, SessionDep
from app.models.tables import Generation, Prompt
from app.schemas.compress import GenerateRequest, GenerateResponse
from app.services.compression_service import compress_prompt
from app.services.llm_adapter import chat_complete

router = APIRouter(prefix="/generate", tags=["generate"])


@router.post("", response_model=GenerateResponse)
async def generate(
    body: GenerateRequest,
    session: SessionDep,
    user: OptionalUser,
) -> GenerateResponse:
    c = compress_prompt(
        body.prompt,
        body.mode,
        body.compression_level,
        estimate_only=False,
    )
    llm = await chat_complete(c.compressed_prompt)
    uid = user.id if user else None
    pid = uuid4()
    session.add(Prompt(id=pid, user_id=uid, original_text=body.prompt))
    session.add(
        Generation(
            id=uuid4(),
            prompt_id=pid,
            response_text=llm["output"],
            latency_ms=llm["latency_ms"],
            tokens_used=llm.get("tokens_used"),
        )
    )
    await session.commit()
    return GenerateResponse(
        output=llm["output"],
        latency_ms=llm["latency_ms"],
        tokens_used=int(llm.get("tokens_used") or 0),
    )
