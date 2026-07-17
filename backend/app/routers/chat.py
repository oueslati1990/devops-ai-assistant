from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.llm import run_with_tools
from app.config import LLM_MODEL
from app.constants import MAX_HISTORY, SYSTEM_PROMPT

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest) -> StreamingResponse:
    model = req.model or LLM_MODEL
    messages = build_messages(req.history, req.message)
    return StreamingResponse(run_with_tools(messages, model), media_type="text/plain")


def build_messages(history: list[dict], user_message: str) -> list[dict]:
    history_trimmed = trim_history(history)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history_trimmed,
        {"role": "user", "content": user_message},
    ]
    return messages


def trim_history(history: list[dict]) -> list[dict]:
    return history[-MAX_HISTORY:]
