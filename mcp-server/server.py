from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
import asyncio

from tools.git_tools import git_read

app = Server("Devops ai assistant")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="git_read",
            description="Read Git repository information: commit history, diff, status, branches",
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_path": {
                        "type": "string",
                        "description": "Absolute path to the git repository",
                    },
                    "command": {
                        "type": "string",
                        "description": "Git subcommand, e.g. 'log --oneline -10'",
                    },
                },
                "required": ["repo_path", "command"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "git_read":
        result = git_read(arguments["repo_path"], arguments["command"])
    else:
        result = f"Unknown tool: {name}"
    return [types.TextContent(type="text", text=result)]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
