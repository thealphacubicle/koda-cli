"""Git operations for koda CLI."""

import subprocess


def init_repo(path: str) -> bool:
    """Initialize git repository at path. Returns True on success."""
    result = subprocess.run(
        ["git", "init"],
        cwd=path,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def first_commit(path: str) -> bool:
    """Stage all files and make initial commit. Returns True on success."""
    add_result = subprocess.run(
        ["git", "add", "."],
        cwd=path,
        capture_output=True,
        text=True,
    )
    if add_result.returncode != 0:
        return False

    commit_result = subprocess.run(
        ["git", "commit", "-m", "Initial commit via koda"],
        cwd=path,
        capture_output=True,
        text=True,
    )
    return commit_result.returncode == 0


def create_and_push(path: str, name: str) -> bool:
    """Create GitHub repo via gh and push. Returns True on success."""
    result = subprocess.run(
        ["gh", "repo", "create", name, "--source", path, "--push"],
        cwd=path,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0
