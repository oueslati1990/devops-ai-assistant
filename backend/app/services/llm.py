import json
from collections.abc import AsyncGenerator

import httpx

from app.config import LLM_BASE_URL
from app.mcp_client import get_tool_definitions, call_tool


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


async def _llm_call(messages: list[dict], model: str, tools: list[dict]):
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            f"{LLM_BASE_URL}/v1/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "tools": tools,
                "stream": False,
            },
        )
        resp.raise_for_status()
        return resp.json()


async def run_with_tools(messages: list[dict], model: str) -> AsyncGenerator[str, None]:
    tools = await get_tool_definitions()
    response = await _llm_call(messages, model, tools)
    choice = response["choices"][0]

    if choice.get("finish_reason") == "tool_calls":
        assitant_msg = choice["message"]
        messages.append(assitant_msg)

        for tc in assitant_msg["tool_calls"]:
            name = tc["function"]["name"]
            arguments = json.loads(tc["function"]["arguments"])
            tool_resp = await call_tool(name, arguments)

            messages.append(
                {"role": "tool", "tool_call_id": tc["id"], "content": tool_resp}
            )

        async for chunck in stream_llm_response(messages, model):
            yield chunck
    else:
        yield choice["message"].get("content", "")
