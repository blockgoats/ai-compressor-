from fastapi import APIRouter

from app.api.deps import SessionDep
from app.services import analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
async def analytics_overview(session: SessionDep) -> dict:
    return await analytics_service.overview(session)


@router.get("/history")
async def analytics_history(session: SessionDep, days: int = 14) -> list[dict]:
    return await analytics_service.history_series(session, days=days)


@router.get("/recent")
async def analytics_recent(session: SessionDep, limit: int = 10) -> list[dict]:
    return await analytics_service.recent_activity(session, limit=limit)
