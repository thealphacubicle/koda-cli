"""Web app project template."""

from __future__ import annotations


def get_structure(project_name: str) -> list[tuple[str, str | None]]:
    """Return folder structure for a web app project.
    Each tuple is (path, content) where content is None for directories.
    Paths are relative to project root.
    """
    index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="app"></div>
    <script src="app.js"></script>
</body>
</html>
"""
    style_css = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: system-ui, sans-serif;
    line-height: 1.5;
}
"""
    app_js = """document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    app.textContent = 'Hello, World!';
});
"""
    return [
        (f"{project_name}/src", None),
        (f"{project_name}/src/index.html", index_html),
        (f"{project_name}/src/style.css", style_css),
        (f"{project_name}/src/app.js", app_js),
        (f"{project_name}/assets", None),
        (
            f"{project_name}/.gitignore",
            "node_modules/\n.DS_Store\n",
        ),
        (
            f"{project_name}/README.md",
            "<!-- AI will fill this -->\n",
        ),
    ]
