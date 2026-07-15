from fastmcp import Client

_client = Client("../../mcp-server/server.py")


async def call_tool(name: str, arguments: dict) -> str:
    async with _client:
        result = await _client.call_tool(name, arguments)
        return result[0].text  # first content block


async def get_tool_definitions() -> list:
    async with _client:
        return await _client.list_tools()
