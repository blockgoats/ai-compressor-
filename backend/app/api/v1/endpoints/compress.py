from uuid import uuid4

from fastapi import APIRouter

from app.api.deps import OptionalUser, SessionDep
from app.models.tables import AnalyticsEvent, CompressedPrompt, Prompt
from app.schemas.compress import CompressRequest, CompressResponse
from app.services.compression_service import compress_prompt

router = APIRouter(prefix="/compress", tags=["compress"])


@router.post("", response_model=CompressResponse)
async def post_compress(
    body: CompressRequest,
    session: SessionDep,
    user: OptionalUser,
) -> CompressResponse:
    result = compress_prompt(
        body.prompt,
        body.mode,
        body.compression_level,
        estimate_only=False,
    )

    uid = user.id if user else None
    pid = uuid4()
    session.add(Prompt(id=pid, user_id=uid, original_text=body.prompt))
    session.add(
        CompressedPrompt(
            id=uuid4(),
            prompt_id=pid,
            compressed_text=result.compressed_prompt,
            mode=body.mode,
            compression_ratio=result.compression_ratio,
            tokens_before=result.tokens_before,
            tokens_after=result.tokens_after,
        )
    )
    saved = max(0, result.tokens_before - result.tokens_after)
    cost = saved * 1.2e-6
    session.add(
        AnalyticsEvent(
            id=uuid4(),
            user_id=uid,
            tokens_before=result.tokens_before,
            tokens_after=result.tokens_after,
            cost_estimate=cost,
            meta={"mode": body.mode, "level": body.compression_level},
        )
    )
    await session.commit()

    return CompressResponse(
        compressed_prompt=result.compressed_prompt,
        tokens_before=result.tokens_before,
        tokens_after=result.tokens_after,
        compression_ratio=result.compression_ratio,
        insights=result.insights,
    )
