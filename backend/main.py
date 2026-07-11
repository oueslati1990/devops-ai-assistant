import os
import httpx
import json

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from constants import Constants

load_dotenv()
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


app = FastAPI(title="AI Devops Assistant")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    messages = [{"role": "system", "content": Constants.SYSTEM_PROMPT}]
    messages += req.history
    messages.append({"role": "user", "content": req.message})

    async def stream_response():
        async with httpx.AsyncClient(timeout=120) as client:
            async with client.stream(
                "POST",
                LLM_BASE_URL,
                json={
                    "model": LLM_MODEL,
                    "messages": messages,
                    "stream": True,
                },
            ) as resp:
                async for line in resp.aiter_lines():
                    if line.startswith("data: ") and line != "data: [DONE]":
                        data = json.loads(line[6:])
                        delta = data["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta

    return StreamingResponse(stream_response(), media_type="text/plain")
