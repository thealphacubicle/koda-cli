"""Project scaffolding - creates folder structures from templates."""

import os
import importlib
import sys

from core.utils import typewrite, GREEN, RESET


def create_project(name: str, project_type: str, path: str) -> str:
    """Create project folder structure from template.
    Streams each file/folder as it's created.
    Returns the full path to the created project.
    """
    # Map project_type to template module name
    type_to_module = {
        "datascience": "datascience",
        "api": "api",
        "webapp": "webapp",
    }
    module_name = type_to_module.get(project_type, "api")
    template_module = importlib.import_module(f"templates.{module_name}")
    structure = template_module.get_structure(name)

    base_path = os.path.abspath(path)
    project_path = os.path.join(base_path, name)

    for entry_path, content in structure:
        full_path = os.path.join(base_path, entry_path)

        if content is None:
            # Directory
            os.makedirs(full_path, exist_ok=True)
            rel_path = entry_path
        else:
            # File - ensure parent dir exists
            parent = os.path.dirname(full_path)
            os.makedirs(parent, exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
            rel_path = entry_path

        typewrite(f"  {GREEN}✓{RESET} Created {rel_path}", delay=0.01)

    return project_path
