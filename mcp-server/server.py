from mcp.server.fastmcp import FastMCP
from tools.git_tools import git_read as _git_read

mcp = FastMCP("Devops ai assistant")


@mcp.tool()
def git_read(repo_path: str, command: str) -> str:
    """Read Git repository information: commit history, diff, status, branches.

    Args:
        repo_path: Absolute path to the git repository.
        command: Git subcommand, e.g. 'log --oneline -10' or 'status'.
    """
    return _git_read(repo_path, command)


if __name__ == "__main__":
    mcp.run()
