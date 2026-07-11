from fastapi import FastAPI
import httpx
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


app = FastAPI(title="AI Devops Assistant")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            "http://localhost:11434/v1/chat/completions",
            json={
                "model": "llama3.2",
                "messages": [{"role": "user", "content": req.message}],
                "stream": False,
            },
        )
    answer = resp.json()["choices"][0]["message"]["content"]
    return {"answer": answer}
