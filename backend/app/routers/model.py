from fastapi import APIRouter
import httpx
from app.config import LLM_BASE_URL

router = APIRouter()


@router.get("/models")
async def list_models():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{LLM_BASE_URL}/api/tags")
        models = [m["name"] for m in resp.json()["models"]]
        return {"models": models}
