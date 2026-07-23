from mcp.server.fastmcp import FastMCP
from tools.git_tools import git_read as _git_read
from tools.log_tools import analyze_logs as _analyze_logs
from tools.yaml_tools import generate_yaml as _generate_yaml

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


@mcp.tool()
def generate_yaml(type: str, params: dict) -> str:
    """Generate a YAML manifest for a given Kubernetes or DevOps resource type.

    Args:
        type: Resource kind to generate. Supported values: 'deployment', 'service',
              'configmap', 'ingress', 'cronjob'.
        params: Key/value pairs that populate the manifest, e.g.
                {"name": "my-app", "image": "nginx:latest", "replicas": 3}.

    Returns:
        A YAML string ready to apply with kubectl or include in a Helm chart.
    """
    return _generate_yaml(type, params)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
