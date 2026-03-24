from fastapi import APIRouter

router = APIRouter(prefix="/demo", tags=["meta"])


@router.get("/prompts")
async def demo_prompts() -> dict[str, list[str]]:
    return {
        "samples": [
            "You are an expert assistant. Summarize the paper focusing on methodology.",
            "Refactor this TypeScript for clarity and fewer tokens.",
        ]
    }
