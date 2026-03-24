from fastapi import APIRouter

from app.api.v1.endpoints import (
    analytics,
    auth,
    compress,
    cost_simulate,
    demo,
    generate,
    health,
    meta,
    playground_sessions,
    prompt_versions,
    replay,
    token_estimate,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(meta.router)
api_router.include_router(auth.router)
api_router.include_router(compress.router)
api_router.include_router(token_estimate.router)
api_router.include_router(generate.router)
api_router.include_router(analytics.router)
api_router.include_router(cost_simulate.router)
api_router.include_router(replay.router)
api_router.include_router(demo.router)
api_router.include_router(playground_sessions.router)
api_router.include_router(prompt_versions.router)
