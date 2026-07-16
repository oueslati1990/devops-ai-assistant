import json
import logging
import time
from collections.abc import AsyncGenerator

import httpx

from app.config import LLM_BASE_URL
from app.mcp_client import get_tool_definitions, call_tool
from app.constants import MAX_TOOL_ITERATIONS

logger = logging.getLogger(__name__)


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
    t0 = time.perf_counter()
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
        data = resp.json()
    elapsed = time.perf_counter() - t0
    usage = data.get("usage", {})
    logger.info(
        "LLM call: model=%s latency=%.2fs prompt_tokens=%s completion_tokens=%s",
        model,
        elapsed,
        usage.get("prompt_tokens", "n/a"),
        usage.get("completion_tokens", "n/a"),
    )
    return data


async def run_with_tools(messages: list[dict], model: str) -> AsyncGenerator[str, None]:
    logger.info("run_with_tools: model=%s context_messages=%d", model, len(messages))

    tools = await get_tool_definitions()
    logger.debug(
        "Loaded %d tool(s) from MCP server: %s",
        len(tools),
        [t["function"]["name"] for t in tools],
    )

    for iteration in range(MAX_TOOL_ITERATIONS):
        response = await _llm_call(messages, model, tools)
        choice = response["choices"][0]
        finish_reason = choice.get("finish_reason")
        logger.info(
            "finish_reason=%s (iteration %d/%d)",
            finish_reason,
            iteration + 1,
            MAX_TOOL_ITERATIONS,
        )

        if finish_reason != "tool_calls":
            async for chunk in stream_llm_response(messages, model):
                yield chunk
            return

        assistant_msg = choice["message"]
        tool_calls = assistant_msg.get("tool_calls", [])
        logger.info("Dispatching %d tool call(s)", len(tool_calls))
        messages.append(assistant_msg)

        for tc in tool_calls:
            name = tc["function"]["name"]
            arguments = json.loads(tc["function"]["arguments"])
            logger.debug("Tool call: name=%s args=%s", name, arguments)

            tool_resp = await call_tool(name, arguments)
            logger.debug("Tool response: name=%s size=%d chars", name, len(tool_resp))

            messages.append(
                {"role": "tool", "tool_call_id": tc["id"], "content": tool_resp}
            )

    logger.warning(
        "Max tool iterations (%d) reached, forcing final response", MAX_TOOL_ITERATIONS
    )
    async for chunk in stream_llm_response(messages, model):
        yield chunk
