from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.constants import SYSTEM_PROMPT
from app.schemas.chat import ChatRequest
from app.services.llm import stream_llm_response
from app.config import LLM_MODEL

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest) -> StreamingResponse:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *req.history,
        {"role": "user", "content": req.message},
    ]
    model = req.model or LLM_MODEL
    return StreamingResponse(
        stream_llm_response(messages, model), media_type="text/plain"
    )
