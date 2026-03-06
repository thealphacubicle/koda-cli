"""Data science project template."""

from __future__ import annotations


def get_structure(project_name: str) -> list[tuple[str, str | None]]:
    """Return folder structure for a data science project.
    Each tuple is (path, content) where content is None for directories.
    Paths are relative to project root.
    """
    return [
        (f"{project_name}/data/raw", None),
        (f"{project_name}/data/processed", None),
        (f"{project_name}/notebooks", None),
        (f"{project_name}/src", None),
        (f"{project_name}/models", None),
        (
            f"{project_name}/requirements.txt",
            "pandas\nnumpy\nmatplotlib\nscikit-learn\njupyter\n",
        ),
        (
            f"{project_name}/.gitignore",
            "venv/\n__pycache__/\n.ipynb_checkpoints/\n*.pyc\ndata/\n",
        ),
        (
            f"{project_name}/README.md",
            "<!-- AI will fill this -->\n",
        ),
    ]
