"""Celery app for heavy compression / analytics (c.md)."""

from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "ramanujan",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)


@celery_app.task(name="aggregate_analytics")
def aggregate_analytics() -> str:
    """Placeholder: nightly analytics aggregation."""
    return "ok"


@celery_app.task(name="heavy_compress")
def heavy_compress_job(prompt_id: str) -> dict[str, str]:
    """Placeholder for heavy compression offloaded from API."""
    return {"status": "queued", "prompt_id": prompt_id}
