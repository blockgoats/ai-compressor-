from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = "Ramanujan Compression API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+asyncpg://ram:ram@localhost:5432/ramanujan"
    sync_database_url: str = "postgresql://ram:ram@localhost:5432/ramanujan"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    secret_key: str = "change-me-in-production-use-openssl-rand-hex-32"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7

    # Auth (dev)
    auth_disable: bool = False

    # HuggingFace tokenizer base (for encode/decode pipeline)
    base_tokenizer_name: str = "bert-base-uncased"

    # Paper-aligned diagnostics (Ramanujan projections on token IDs; optional)
    rcp_spectral_max_tokens: int = 512
    rcp_spectral_max_q: int = 32

    # LLM / OpenAI-compatible
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    groq_api_key: str | None = None
    groq_base_url: str = "https://api.groq.com/openai/v1"
    llm_provider: str = "openai"  # openai | groq

    # Rate limit
    rate_limit_per_minute: int = 120

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"


@lru_cache
def get_settings() -> Settings:
    return Settings()
