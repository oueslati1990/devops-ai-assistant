import os
from fastmcp import Client

_SERVER_PATH = os.path.join(os.path.dirname(__file__), "../../mcp-server/server.py")
_client = Client(_SERVER_PATH)


async def call_tool(name: str, arguments: dict) -> str:
    async with _client:
        result = await _client.call_tool(name, arguments)
        return result[0].text


async def get_tool_definitions() -> list[dict]:
    async with _client:
        tools = await _client.list_tools()
    return [
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
