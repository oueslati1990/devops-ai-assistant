from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.constants import SYSTEM_PROMPT
from app.schemas.chat import ChatRequest
from app.services.llm import stream_llm_response

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest) -> StreamingResponse:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *req.history,
        {"role": "user", "content": req.message},
    ]
    return StreamingResponse(stream_llm_response(messages), media_type="text/plain")
