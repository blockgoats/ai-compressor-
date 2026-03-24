from fastapi import APIRouter

from app.schemas.compress import CompressRequest, ReplayPayload

router = APIRouter(prefix="/replay-payload", tags=["meta"])


@router.post("", response_model=ReplayPayload)
async def replay_payload(body: CompressRequest) -> ReplayPayload:
    """Exact JSON body for POST /api/v1/compress (reproducibility)."""
    return ReplayPayload(
        endpoint="/api/v1/compress",
        method="POST",
        body=body.model_dump(),
    )
