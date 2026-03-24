"""Runtime metadata for dashboards (models, provider)."""

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/models")
def models_catalog() -> dict:
    settings = get_settings()
    default_openai = settings.openai_model
    default_groq = "llama-3.1-8b-instant"
    active = default_groq if settings.llm_provider == "groq" else default_openai
    rows = [
        {
            "id": "gpt-4.1",
            "label": "GPT-4.1",
            "provider": "openai",
            "cost_hint": "$5 / 1M in",
            "latency_hint": "~420ms p50",
            "compat": "Excellent",
        },
        {
            "id": "gpt-4o",
            "label": "GPT-4o",
            "provider": "openai",
            "cost_hint": "$2.5 / 1M in",
            "latency_hint": "~280ms p50",
            "compat": "Excellent",
        },
        {
            "id": "gpt-4o-mini",
            "label": "GPT-4o mini",
            "provider": "openai",
            "cost_hint": "$0.15 / 1M in",
            "latency_hint": "~200ms p50",
            "compat": "Excellent",
        },
        {
            "id": "claude-3-5-sonnet-20241022",
            "label": "Claude 3.5 Sonnet",
            "provider": "anthropic",
            "cost_hint": "$3 / 1M in",
            "latency_hint": "~360ms p50",
            "compat": "Strong",
        },
        {
            "id": "llama-3.1-8b-instant",
            "label": "Llama 3.1 8B Instant",
            "provider": "groq",
            "cost_hint": "$0.05 / 1M in",
            "latency_hint": "~120ms p50",
            "compat": "Good",
        },
    ]
    for r in rows:
        r["is_default"] = r["id"] == active
    return {
        "llm_provider": settings.llm_provider,
        "default_model_id": active,
        "openai_model": default_openai,
        "groq_default_model": default_groq,
        "models": rows,
    }
