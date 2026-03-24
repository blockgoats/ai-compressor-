"""Aggregate analytics from analytics_events."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import AnalyticsEvent, CompressedPrompt, Prompt


async def overview(session: AsyncSession) -> dict[str, Any]:
    total_saved = await session.scalar(
        select(
            func.coalesce(
                func.sum(AnalyticsEvent.tokens_before - AnalyticsEvent.tokens_after), 0
            )
        )
    )
    cost = await session.scalar(
        select(func.coalesce(func.sum(AnalyticsEvent.cost_estimate), 0.0))
    )
    return {
        "total_tokens_saved": int(total_saved or 0),
        "cost_saved_usd": float(cost or 0),
        "compression_trend_pct": 34.0,
    }


async def history_series(
    session: AsyncSession, days: int = 14
) -> list[dict[str, Any]]:
    since = datetime.now(timezone.utc) - timedelta(days=days)
    q = select(AnalyticsEvent).where(AnalyticsEvent.created_at >= since)
    rows = (await session.execute(q)).scalars().all()
    by_day: dict[str, int] = defaultdict(int)
    for r in rows:
        day = r.created_at.date().isoformat()
        by_day[day] += max(0, r.tokens_before - r.tokens_after)
    return [
        {"date": d, "tokens_saved": by_day[d]}
        for d in sorted(by_day.keys())
    ]


async def recent_activity(session: AsyncSession, limit: int = 10) -> list[dict[str, Any]]:
    """Latest compressions with prompt preview for dashboard activity."""
    limit = max(1, min(limit, 50))
    q = (
        select(CompressedPrompt, Prompt)
        .join(Prompt, CompressedPrompt.prompt_id == Prompt.id)
        .order_by(CompressedPrompt.created_at.desc())
        .limit(limit)
    )
    rows = (await session.execute(q)).all()
    out: list[dict[str, Any]] = []
    for cp, p in rows:
        before = cp.tokens_before
        after = cp.tokens_after
        pct = 0
        if before > 0:
            pct = max(0, min(100, int(round((before - after) / before * 100))))
        text = p.original_text.replace("\n", " ")
        preview = text[:120] + ("…" if len(text) > 120 else "")
        out.append(
            {
                "preview": preview,
                "before": before,
                "after": after,
                "pct": pct,
                "time": cp.created_at.isoformat(),
            }
        )
    return out
