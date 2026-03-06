"""Python API project template."""

from __future__ import annotations


def get_structure(project_name: str) -> list[tuple[str, str | None]]:
    """Return folder structure for a Python API project.
    Each tuple is (path, content) where content is None for directories.
    Paths are relative to project root.
    """
    main_py = '''"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/health")
def health():
    return {"status": "ok"}
'''
    dockerfile = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    return [
        (f"{project_name}/src", None),
        (f"{project_name}/src/main.py", main_py),
        (f"{project_name}/src/routes", None),
        (f"{project_name}/src/models", None),
        (f"{project_name}/tests", None),
        (
            f"{project_name}/requirements.txt",
            "fastapi\nuvicorn\npydantic\n",
        ),
        (
            f"{project_name}/.gitignore",
            "venv/\n__pycache__/\n*.pyc\n.env\n",
        ),
        (f"{project_name}/Dockerfile", dockerfile),
        (
            f"{project_name}/README.md",
            "<!-- AI will fill this -->\n",
        ),
    ]
