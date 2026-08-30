from fastmcp import Client
import logging
import time
from app.config import MCP_SERVER_URL

logger = logging.getLogger(__name__)

_client = Client(MCP_SERVER_URL)
_tool_definitions: list[dict] | None = None
_tool_definitions_fetched_at: float = 0.0
_TOOL_CACHE_TTL = 300  # seconds


async def call_tool(name: str, arguments: dict) -> str:
    async with _client:
        result = await _client.call_tool(name, arguments)
        logger.debug("call_tool result: name=%s result=%s", name, result.content[0])
        return result.content[0].text


async def get_tool_definitions() -> list[dict]:
    global _tool_definitions, _tool_definitions_fetched_at
    if _tool_definitions is not None and time.monotonic() - _tool_definitions_fetched_at < _TOOL_CACHE_TTL:
        return _tool_definitions
    async with _client:
        tools = await _client.list_tools()
    _tool_definitions = [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.inputSchema,
            },
        }
        for t in tools
    ]
    _tool_definitions_fetched_at = time.monotonic()
    logger.info("Cached %d tool definition(s) from MCP server (TTL=%ds)", len(_tool_definitions), _TOOL_CACHE_TTL)
    return _tool_definitions
