from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import chat, model
from app.config import LLM_MODEL

app = FastAPI(title="AI Devops Assistant")
app.include_router(chat.router)
app.include_router(model.router)
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "model": LLM_MODEL}
