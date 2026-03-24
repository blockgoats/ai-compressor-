"""
Compression pipeline: text preprocessing + HF tokenization + ramanujan_compression.

Maps c.md modes to SDK CompressionStrategy / CompressionConfig.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Literal

from transformers import AutoTokenizer

from app.core.config import get_settings
from app.services.ramanujan_spectral import spectral_energy_metrics
from ramanujan_compression import (
    CompressionConfig,
    CompressionStrategy,
    RamanujanCompressor,
)

CompressMode = Literal["lossless", "lossy", "ramanujan"]
Level = Literal["low", "medium", "aggressive"]


@dataclass
class CompressionResult:
    compressed_prompt: str
    tokens_before: int
    tokens_after: int
    compression_ratio: float
    insights: dict[str, Any]


def _level_to_ratio(level: Level) -> float:
    return {"low": 0.85, "medium": 0.5, "aggressive": 0.28}[level]


def _mode_to_strategy(mode: CompressMode) -> CompressionStrategy:
    if mode == "lossless":
        return CompressionStrategy.HYBRID
    if mode == "ramanujan":
        return CompressionStrategy.SPARSE_MODULAR
    return CompressionStrategy.HYBRID


def _build_config(mode: CompressMode, level: Level, token_count: int) -> CompressionConfig:
    ratio = _level_to_ratio(level)
    if mode == "lossless":
        ratio = max(0.92, ratio)
    strategy = _mode_to_strategy(mode)
    modular = 11 if mode == "ramanujan" else 7
    sparse = 0.06 if mode == "ramanujan" else 0.1
    ctx = max(64, min(token_count, 4096))
    return CompressionConfig(
        strategy=strategy,
        compression_ratio=ratio,
        modular_base=modular,
        sparse_threshold=sparse,
        context_length=ctx,
        gpu_acceleration=False,
    )


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _simple_patterns(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    top = sorted(freq.items(), key=lambda x: -x[1])[:8]
    return [f"{w} (×{c})" for w, c in top if c > 1]


@lru_cache(maxsize=2)
def _tokenizer(name: str):
    return AutoTokenizer.from_pretrained(name)


def compress_prompt(
    prompt: str,
    mode: CompressMode,
    compression_level: Level,
    *,
    estimate_only: bool = False,
) -> CompressionResult:
    """
    Run compression. If estimate_only, skip heavy compressor (token count only).
    """
    settings = get_settings()
    tok = _tokenizer(settings.base_tokenizer_name)

    cleaned = _normalize_whitespace(prompt)
    ids = tok.encode(cleaned, add_special_tokens=False)
    tokens_before = max(1, len(ids))

    if estimate_only:
        ratio_est = _level_to_ratio(compression_level)
        if mode == "lossless":
            tokens_after = max(1, int(tokens_before * 0.98))
        else:
            tokens_after = max(1, int(tokens_before * (0.35 + ratio_est * 0.5)))
        cr = tokens_after / tokens_before
        return CompressionResult(
            compressed_prompt=cleaned,
            tokens_before=tokens_before,
            tokens_after=tokens_after,
            compression_ratio=cr,
            insights={
                "removed_tokens": [],
                "patterns_detected": _simple_patterns(cleaned),
                "math_score": round(min(0.99, 0.4 + (1 - cr) * 0.5), 4),
            },
        )

    if mode == "lossless":
        compressed_text = cleaned
        out_ids = tok.encode(compressed_text, add_special_tokens=False)
        tokens_after = max(1, len(out_ids))
        cr = tokens_after / tokens_before
        return CompressionResult(
            compressed_prompt=compressed_text,
            tokens_before=tokens_before,
            tokens_after=tokens_after,
            compression_ratio=cr,
            insights={
                "removed_tokens": [],
                "patterns_detected": _simple_patterns(cleaned),
                "math_score": round(0.55 + (1 - cr) * 0.1, 4),
            },
        )

    cfg = _build_config(mode, compression_level, tokens_before)
    compressor = RamanujanCompressor(cfg)
    compressed = compressor.compress(ids)
    out_ids = compressed["compressed"]
    tokens_after = max(1, len(out_ids))

    compressed_text = tok.decode(out_ids, skip_special_tokens=True)
    if not compressed_text.strip():
        compressed_text = cleaned[: max(1, len(cleaned) // 2)] + "…"

    cr = tokens_after / tokens_before
    stats = compressor.get_compression_stats(ids, compressed)
    math_score = round(min(0.99, float(stats.get("space_saved", 0)) + 0.35), 4)

    removed: list[str] = []
    if len(ids) != len(out_ids):
        removed = [f"token_delta:{len(ids) - len(out_ids)}"]

    meta = compressed.get("metadata") or {}
    spectral = spectral_energy_metrics(
        list(ids),
        max_q=settings.rcp_spectral_max_q,
        max_len=settings.rcp_spectral_max_tokens,
    )
    paper_aligned: dict[str, Any] = {}
    if spectral:
        paper_aligned["spectral"] = spectral

    insights: dict[str, Any] = {
        "removed_tokens": removed,
        "patterns_detected": _simple_patterns(cleaned),
        "math_score": math_score,
        "strategy": cfg.strategy.value,
        "compressor_metadata": meta,
        "compression_stats": {
            "original_length": stats.get("original_length"),
            "compressed_length": stats.get("compressed_length"),
            "compression_ratio": round(float(stats.get("compression_ratio", 0)), 6),
            "space_saved": round(float(stats.get("space_saved", 0)), 6),
            "bits_per_token": round(float(stats.get("bits_per_token", 0)), 6),
        },
    }
    if paper_aligned:
        insights["paper_aligned"] = paper_aligned

    return CompressionResult(
        compressed_prompt=compressed_text,
        tokens_before=tokens_before,
        tokens_after=tokens_after,
        compression_ratio=float(cr),
        insights=insights,
    )
