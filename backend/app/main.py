from fastapi import FastAPI

from app.routers import chat

app = FastAPI(title="AI Devops Assistant")
app.include_router(chat.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
