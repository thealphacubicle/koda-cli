"""Tool authentication checker for koda CLI."""

import shutil
import subprocess

from core.utils import GREEN, RESET, YELLOW, typewrite


def check_gh() -> bool:
    """Check if gh CLI is logged in. If not, run gh auth login."""
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return True
    # Not logged in - run interactive login
    typewrite(f"  {YELLOW}⚠{RESET} GitHub CLI not logged in. Starting gh auth login...", delay=0.01)
    login_result = subprocess.run(
        ["gh", "auth", "login"],
        stdin=None,  # Interactive
    )
    return login_result.returncode == 0


def check_claude_code() -> bool:
    """Check if Claude Code is installed and authenticated. Install if not."""
    claude_path = shutil.which("claude")
    if claude_path is None:
        typewrite(f"  {YELLOW}⚠{RESET} Claude Code not found. Installing...", delay=0.01)
        install_result = subprocess.run(
            ["npm", "install", "-g", "@anthropic-ai/claude-code"],
            capture_output=True,
            text=True,
        )
        if install_result.returncode != 0:
            typewrite(
                f"  {YELLOW}⚠{RESET} npm install failed. Run manually: "
                "npm install -g @anthropic-ai/claude-code",
                delay=0.01,
            )
            return False
        typewrite(f"  {GREEN}✓{RESET} Claude Code installed.", delay=0.01)

    # Verify claude is accessible and authenticated
    result = subprocess.run(
        ["claude", "--version"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        typewrite(f"  {YELLOW}⚠{RESET} Claude Code not authenticated. Run: claude", delay=0.01)
        return False
    return True


def check_all() -> bool:
    """Run both checks with streaming status output. Returns True if all pass."""
    all_ok = True

    typewrite("  Checking GitHub CLI...", delay=0.01)
    if check_gh():
        typewrite(f"  {GREEN}✓{RESET} GitHub CLI ready", delay=0.01)
    else:
        typewrite(f"  {YELLOW}⚠{RESET} GitHub CLI not ready", delay=0.01)
        all_ok = False

    typewrite("  Checking Claude Code...", delay=0.01)
    if check_claude_code():
        typewrite(f"  {GREEN}✓{RESET} Claude Code ready", delay=0.01)
    else:
        typewrite(f"  {YELLOW}⚠{RESET} Claude Code not ready", delay=0.01)
        all_ok = False

    return all_ok
