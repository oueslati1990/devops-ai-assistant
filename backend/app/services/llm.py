import json
from collections.abc import AsyncGenerator

import httpx

from app.config import LLM_BASE_URL


async def stream_llm_response(
    messages: list[dict], model: str
) -> AsyncGenerator[str, None]:
    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream(
            "POST",
            f"{LLM_BASE_URL}/v1/chat/completions",
            json={"model": model, "messages": messages, "stream": True},
        ) as resp:
            async for line in resp.aiter_lines():
                if line.startswith("data: ") and line != "data: [DONE]":
                    try:
                        data = json.loads(line[6:])
                        delta = data["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except (json.JSONDecodeError, KeyError):
                        continue
