from fastapi import APIRouter

from app.schemas.compress import CostSimulateRequest, CostSimulateResponse

router = APIRouter(prefix="/cost-simulate", tags=["analytics"])


@router.post("", response_model=CostSimulateResponse)
async def cost_simulate(body: CostSimulateRequest) -> CostSimulateResponse:
    cost_per_1k = 0.012
    without = (body.monthly_tokens / 1000.0) * cost_per_1k
    save_rate = 0.34
    with_c = without * (1 - save_rate)
    pct = int(save_rate * 100) if without > 0 else 0
    return CostSimulateResponse(
        cost_without_compression_usd=round(without, 2),
        cost_with_compression_usd=round(with_c, 2),
        savings_pct=pct,
    )
