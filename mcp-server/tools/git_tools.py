import subprocess, shlex

ALLOWED_GIT_COMMANDS = {
    "log",
    "diff",
    "status",
    "branch",
    "show",
    "ls-files",
    "shortlog",
    "tag",
    "remote",
}


def git_read(repo_path: str, command: str) -> str:
    parts = shlex.split(command)
    if not parts or parts[0] not in ALLOWED_GIT_COMMANDS:
        return f"Error: '{parts[0] if parts else ''}' not allowed. Allowed: {', '.join(sorted(ALLOWED_GIT_COMMANDS))}"

    try:
        result = subprocess.run(
            ["git", "-C", repo_path] + parts,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode != 0:
            return f"Git error:\n{result.stderr}"
        return result.stdout or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: git command timed out"
    except FileNotFoundError:
        return f"Error: repository not found at {repo_path}"
