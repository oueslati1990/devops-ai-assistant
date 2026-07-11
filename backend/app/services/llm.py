import json
from collections.abc import AsyncGenerator

import httpx

from app.config import LLM_BASE_URL, LLM_MODEL


async def stream_llm_response(messages: list[dict]) -> AsyncGenerator[str, None]:
    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream(
            "POST",
            LLM_BASE_URL,
            json={"model": LLM_MODEL, "messages": messages, "stream": True},
        ) as resp:
            async for line in resp.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    data = json.loads(line[6:])
                    delta = data["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
