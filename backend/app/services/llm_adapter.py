"""OpenAI-compatible chat completion for POST /generate."""

from __future__ import annotations

import time
from typing import Any

import httpx

from app.core.config import get_settings


async def chat_complete(
    user_prompt: str,
    *,
    model: str | None = None,
) -> dict[str, Any]:
    settings = get_settings()
    if settings.llm_provider == "groq" and settings.groq_api_key:
        base = settings.groq_base_url.rstrip("/")
        key = settings.groq_api_key
        m = model or "llama-3.1-8b-instant"
    else:
        base = settings.openai_base_url.rstrip("/")
        key = settings.openai_api_key
        m = model or settings.openai_model

    if not key:
        return {
            "output": "[LLM not configured] Set OPENAI_API_KEY or GROQ_API_KEY.",
            "latency_ms": 0,
            "tokens_used": 0,
        }

    url = f"{base}/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": m,
        "messages": [{"role": "user", "content": user_prompt}],
        "temperature": 0.4,
        "max_tokens": 512,
    }
    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post(url, json=body, headers=headers)
        r.raise_for_status()
        data = r.json()
    latency_ms = int((time.perf_counter() - start) * 1000)
    choice = data["choices"][0]["message"]["content"]
    usage = data.get("usage") or {}
    tokens_used = int(usage.get("total_tokens", 0))
    return {
        "output": choice,
        "latency_ms": latency_ms,
        "tokens_used": tokens_used,
    }
