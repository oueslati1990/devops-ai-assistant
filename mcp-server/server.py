from mcp.server.fastmcp import FastMCP
from tools.git_tools import git_read as _git_read
from tools.log_tools import analyze_logs as _analyze_logs

mcp = FastMCP("Devops ai assistant", host="0.0.0.0", port=8001)


@mcp.tool()
def git_read(repo_path: str, command: str) -> str:
    """Read Git repository information: commit history, diff, status, branches.

    Args:
        repo_path: Absolute path to the git repository.
        command: Git subcommand, e.g. 'log --oneline -10' or 'status'.
    """
    return _git_read(repo_path, command)


@mcp.tool()
def analyze_logs(log_content: str, focus: str = "all") -> str:
    """Parses raw logs and extracts errors, warnings

    Args:
        log_content: Content of logs
        focus: extracts errors , warnings or both of them
    """
    return _analyze_logs(log_content, focus)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
