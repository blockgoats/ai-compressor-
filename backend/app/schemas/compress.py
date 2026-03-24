from typing import Any, Literal

from pydantic import BaseModel, Field

CompressMode = Literal["lossless", "lossy", "ramanujan"]
CompressionLevel = Literal["low", "medium", "aggressive"]


class CompressRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=200_000)
    mode: CompressMode = "lossy"
    compression_level: CompressionLevel = "medium"


class CompressInsights(BaseModel):
    removed_tokens: list[str] = []
    patterns_detected: list[str] = []
    math_score: float = 0.0


class CompressResponse(BaseModel):
    compressed_prompt: str
    tokens_before: int
    tokens_after: int
    compression_ratio: float
    insights: dict[str, Any]


class TokenEstimateRequest(BaseModel):
    prompt: str = Field(..., min_length=0, max_length=200_000)
    mode: CompressMode = "lossy"
    compression_level: CompressionLevel = "medium"


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=200_000)
    mode: CompressMode = "lossy"
    compression_level: CompressionLevel = "medium"


class GenerateResponse(BaseModel):
    output: str
    latency_ms: int
    tokens_used: int


class CostSimulateRequest(BaseModel):
    monthly_tokens: int = Field(..., ge=0)


class CostSimulateResponse(BaseModel):
    cost_without_compression_usd: float
    cost_with_compression_usd: float
    savings_pct: int


class ReplayPayload(BaseModel):
    endpoint: str
    method: str
    body: dict[str, Any]
