from fastapi import APIRouter

from app.schemas.compress import CompressResponse, TokenEstimateRequest
from app.services.compression_service import compress_prompt

router = APIRouter(prefix="/token-estimate", tags=["compress"])


@router.post("", response_model=CompressResponse)
async def token_estimate(body: TokenEstimateRequest) -> CompressResponse:
    result = compress_prompt(
        body.prompt,
        body.mode,
        body.compression_level,
        estimate_only=True,
    )
    return CompressResponse(
        compressed_prompt=result.compressed_prompt,
        tokens_before=result.tokens_before,
        tokens_after=result.tokens_after,
        compression_ratio=result.compression_ratio,
        insights=result.insights,
    )
