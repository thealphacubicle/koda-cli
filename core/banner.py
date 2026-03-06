"""Welcome banner for koda CLI."""

import os
import subprocess
import json

# ANSI codes
RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
WHITE = "\033[37m"
DIM = "\033[2m"

CONFIG_PATH = os.path.expanduser("~/.koda/config.json")
TOTAL_WIDTH = 72
LEFT_PANEL_WIDTH = 28
RIGHT_PANEL_WIDTH = 41  # TOTAL_WIDTH - 1 - LEFT_PANEL_WIDTH - 1 - 1 = 72 - 31 = 41


def _get_gh_login() -> str:
    """Get GitHub username via gh api user. Returns 'not logged in' on failure."""
    try:
        result = subprocess.run(
            ["gh", "api", "user", "--jq", ".login"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return "not logged in"


def _get_provider() -> str:
    """Get preferred AI provider from config. Returns 'not set' if none."""
    config_keys = ["anthropic", "openai", "google"]
    display_names = {"anthropic": "Claude", "openai": "OpenAI", "google": "Gemini"}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                config = json.load(f)
            # Check for explicit provider preference
            pref = config.get("provider", "").lower()
            if pref in ["claude", "anthropic"] and config.get("anthropic"):
                return "Claude"
            if pref in ["openai"] and config.get("openai"):
                return "OpenAI"
            if pref in ["gemini", "google"] and config.get("google"):
                return "Gemini"
            # Fallback: first provider with a key
            for key in config_keys:
                if config.get(key):
                    return display_names.get(key, key)
        except Exception:
            pass
    return "not set"


def _get_projects_path() -> str:
    """Get projects path from config. Fallback to ~/Desktop/Projects."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                config = json.load(f)
            path = config.get("projects", "")
            if path:
                return os.path.expanduser(path)
        except Exception:
            pass
    return os.path.expanduser("~/Desktop/Projects")


def _pad(s: str, width: int, truncate: bool = True) -> str:
    """Pad string to width, optionally truncating if too long."""
    if len(s) > width and truncate:
        return s[: width - 3] + "..."
    return s + " " * (width - len(s))


def show_banner() -> None:
    """Display the two-panel welcome banner. Prints instantly (no streaming)."""
    gh_login = _get_gh_login()
    provider = _get_provider()
    projects = _get_projects_path()
    # Truncate projects path if too long (Projects:     = 14 chars, right panel 41, so 41-14=27 for path)
    max_path_len = 27
    projects_display = projects if len(projects) <= max_path_len else "..." + projects[-(max_path_len - 3) :]

    # ASCII art: anvil/hammer logo (28 chars wide)
    logo = [
        "      ▄▄▄▄▄▄▄▄▄▄      ",
        "    ▄████████████▄    ",
        "   ████████████████   ",
        "  █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█  ",
        " ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ",
        "   ▐▄▄▄  ╱▔▔▔╲       ",
        "   ▐███ ▐  ▄▄  █      ",
        "   ▐███  ▀▀▀▀▀▀       ",
    ]

    # KODA in block letters (28 chars wide)
    koda_text = [
        "  ██  ██ ██████ ██████ ██████",
        "  ██ ██  ██  ██ ██  ██ ██  ██",
        "  ████   ██  ██ ██  ██ ██████",
        "  ██ ██  ██  ██ ██  ██ ██  ██",
        "  ██  ██ ██████ ██████ ██  ██",
    ]

    # Right panel lines
    right_lines = [
        ("⚒  Welcome to Koda", CYAN),
        ("─" * 39, DIM),
        (f"Logged in as: {gh_login}", WHITE),
        (f"Provider:     {provider}", WHITE),
        (f"Projects:     {projects_display}", WHITE),
        ("─" * 39, DIM),
        ("Quick commands", DIM),
        ("koda new <name>   start project", WHITE),
        ("koda auth         check logins", WHITE),
        ("koda help         all commands", WHITE),
    ]

    # Build left panel: logo + blank + KODA + v1.0.0
    left_lines = []
    for line in logo:
        left_lines.append(_pad(line, LEFT_PANEL_WIDTH, truncate=False))
    left_lines.append(" " * LEFT_PANEL_WIDTH)  # blank
    for line in koda_text:
        left_lines.append(_pad(line, LEFT_PANEL_WIDTH, truncate=False))
    left_lines.append(_pad("v1.0.0", LEFT_PANEL_WIDTH, truncate=False))

    # Pad right panel lines to RIGHT_PANEL_WIDTH
    right_content = []
    for i, (text, color) in enumerate(right_lines):
        if i in (1, 5):  # dividers - use full width of ─
            padded = "─" * RIGHT_PANEL_WIDTH
        else:
            padded = _pad(text[:RIGHT_PANEL_WIDTH], RIGHT_PANEL_WIDTH, truncate=False)
        right_content.append((padded, color))

    # Ensure both panels have same number of rows (pad with empty lines)
    max_rows = max(len(left_lines), len(right_content))
    while len(left_lines) < max_rows:
        left_lines.append(" " * LEFT_PANEL_WIDTH)
    while len(right_content) < max_rows:
        right_content.append((" " * RIGHT_PANEL_WIDTH, WHITE))

    # Top border: ╭─── Koda v1.0.0 ───...───╮
    top_content = "─── Koda v1.0.0 "
    top_dashes = "─" * (TOTAL_WIDTH - len(top_content) - 2)  # -2 for ╭ and ╮
    top_line = f"╭{top_content}{top_dashes}╮"

    # Bottom border
    bottom_line = "╰" + "─" * (TOTAL_WIDTH - 2) + "╯"

    # Print (instant, no streaming)
    output = []
    output.append(f"{CYAN}{top_line}{RESET}")
    for i in range(max_rows):
        left = left_lines[i]
        right_text, right_color = right_content[i]
        # Color the left: yellow for logo lines (0-7), green for FORGE (8-12), dim for v1.0.0 (13)
        if i < len(logo):
            left_styled = f"{YELLOW}{left}{RESET}"
        elif i < len(logo) + 1 + len(koda_text):
            left_styled = f"{GREEN}{left}{RESET}"
        else:
            left_styled = f"{DIM}{left}{RESET}"
        line = f"{CYAN}│{RESET}{left_styled}{CYAN}│{RESET}{right_color}{right_text}{RESET}{CYAN}│{RESET}"
        output.append(line)
    output.append(f"{CYAN}{bottom_line}{RESET}")

    print("\n".join(output))
