"""Interactive TUI prompts - arrow-key selectors, multiselect, confirm, text input."""

from __future__ import annotations

import os
import select as _select
import sys
import termios
import tty

from core.utils import BOLD, CYAN, DIM, GREEN, RESET


def _is_tty() -> bool:
    """Return True if stdin is a TTY (interactive terminal)."""
    return sys.stdin.isatty()


# Cursor control
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR_FROM_CURSOR = "\033[J"
CLEAR_LINE = "\033[K"  # Clear from cursor to end of line


def _move_up(n: int) -> str:
    """ANSI: move cursor up n lines."""
    return f"\033[{n}A" if n > 0 else ""


def _read_key(fd: int):
    """Read a single keypress. Returns 'up', 'down', 'enter', 'space', or the character."""
    c = os.read(fd, 1).decode("utf-8", errors="replace")
    if not c:
        return None
    if c == "\x1b":
        # Escape sequence - read rest (blocking; arrow keys send \x1b[A or \x1b[B)
        buf = []
        while _select.select([fd], [], [], 0.1)[0]:
            b = os.read(fd, 1)
            if b:
                buf.append(b.decode("utf-8", errors="replace"))
            else:
                break
        seq = "".join(buf)
        if seq in ("[A", "OA"):
            return "up"
        if seq in ("[B", "OB"):
            return "down"
        return None  # plain Escape
    if c in ("\r", "\n"):
        return "enter"
    if c == " ":
        return "space"
    if c == "\x03":  # Ctrl+C
        raise KeyboardInterrupt
    return c


def _setup_raw_mode():
    """Put terminal in raw mode. Returns (fd, old_settings)."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    tty.setraw(fd)
    return fd, old


def _restore_mode(fd, old):
    """Restore terminal to normal mode."""
    termios.tcsetattr(fd, termios.TCSADRAIN, old)


def select_prompt(question: str, options: list[str]) -> str:
    """Single choice — returns the selected string."""
    if not options:
        raise ValueError("options cannot be empty")
    if len(options) == 1:
        return options[0]

    if not _is_tty():
        # Fallback for non-TTY (CI, pipes)
        print(f"  {question}")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        choice = input(f"  Choice [1-{len(options)}]: ").strip() or "1"
        idx = int(choice) - 1 if choice.isdigit() else 0
        idx = max(0, min(idx, len(options) - 1))
        return options[idx]

    fd, old = _setup_raw_mode()
    try:
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.flush()

        current = 0
        n = len(options)
        hint = f"{DIM}↑↓ to move  •  enter to select{RESET}"
        total_lines = 2 + n + 2  # question + blank + options + blank + hint

        def render():
            lines = [f"  {question}", ""]
            for i, opt in enumerate(options):
                if i == current:
                    lines.append(f"  {CYAN}{BOLD}❯ {opt}{RESET}")
                else:
                    lines.append(f"    {DIM}{opt}{RESET}")
            lines.append("")
            lines.append(f"  {hint}")
            return "\n".join(lines), len(lines)

        def write_menu(lines: list[str]):
            """Write menu lines, each at column 0 to avoid stair-step alignment."""
            for line in lines:
                sys.stdout.write("\r" + line + CLEAR_LINE + "\n")
            sys.stdout.flush()

        def redraw():
            text, _ = render()
            sys.stdout.write(_move_up(drawn_lines))
            write_menu(text.split("\n"))

        text, drawn_lines = render()
        lines = text.split("\n")
        write_menu(lines)

        while True:
            key = _read_key(fd)
            if key == "up":
                current = (current - 1) % n
                redraw()
            elif key == "down":
                current = (current + 1) % n
                redraw()
            elif key == "enter":
                break

        # Clear menu and restore
        sys.stdout.write(_move_up(total_lines) + "\r" + CLEAR_FROM_CURSOR)
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()
        return options[current]

    finally:
        _restore_mode(fd, old)
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


def multiselect_prompt(question: str, options: list[str]) -> list[str]:
    """Multiple choice — space to toggle, enter to confirm. Returns list of selected strings."""
    if not options:
        return []

    if not _is_tty():
        # Fallback: default to all selected
        return options[:]

    fd, old = _setup_raw_mode()
    try:
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.flush()

        current = 0
        selected = set(range(len(options)))
        n = len(options)
        hint = f"{DIM}↑↓ move  •  space toggle  •  enter confirm{RESET}"
        total_lines = 2 + n + 2

        def render():
            lines = [f"  {question}", ""]
            for i, opt in enumerate(options):
                mark = f"{GREEN}◉{RESET}" if i in selected else f"{DIM}○{RESET}"
                prefix = f"  {CYAN}{BOLD}❯{RESET} " if i == current else "    "
                opt_text = opt if i in selected else f"{DIM}{opt}{RESET}"
                lines.append(f"{prefix}{mark} {opt_text}")
            lines.append("")
            lines.append(f"  {hint}")
            return "\n".join(lines), len(lines)

        def write_menu(lines: list[str]):
            for line in lines:
                sys.stdout.write("\r" + line + CLEAR_LINE + "\n")
            sys.stdout.flush()

        def redraw():
            text, _ = render()
            sys.stdout.write(_move_up(drawn_lines))
            write_menu(text.split("\n"))

        text, drawn_lines = render()
        write_menu(text.split("\n"))

        while True:
            key = _read_key(fd)
            if key == "up":
                current = (current - 1) % n
                redraw()
            elif key == "down":
                current = (current + 1) % n
                redraw()
            elif key == "space":
                if current in selected:
                    selected.remove(current)
                else:
                    selected.add(current)
                redraw()
            elif key == "enter":
                break

        sys.stdout.write(_move_up(total_lines) + "\r" + CLEAR_FROM_CURSOR)
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()
        return [options[i] for i in sorted(selected)]

    finally:
        _restore_mode(fd, old)
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


def confirm_prompt(question: str) -> bool:
    """Yes/no — returns True or False. Defaults to Yes on Enter."""
    if not _is_tty():
        resp = input(f"  {question} [Y/n]: ").strip().lower()
        return resp != "n" and resp != "no"

    fd, old = _setup_raw_mode()
    try:
        prompt = f"  {question} [Y/n]: "
        sys.stdout.write(prompt)
        sys.stdout.flush()

        while True:
            key = _read_key(fd)
            if key == "enter":
                sys.stdout.write("\n")
                sys.stdout.flush()
                return True
            if key and key.lower() == "y":
                sys.stdout.write("y\n")
                sys.stdout.flush()
                return True
            if key and key.lower() == "n":
                sys.stdout.write("n\n")
                sys.stdout.flush()
                return False

    finally:
        _restore_mode(fd, old)


def text_input_prompt(question: str, default: str | None = None) -> str:
    """Free text input with optional default shown in dim."""
    if default is not None:
        prompt = f"  {question} ({DIM}{default}{RESET}): "
    else:
        prompt = f"  {question}: "
    result = input(prompt).strip()
    if not result and default is not None:
        return default
    return result


# Alias for consistency with user's requested API
def select(question: str, options: list[str]) -> str:
    return select_prompt(question, options)


def multiselect(question: str, options: list[str]) -> list[str]:
    return multiselect_prompt(question, options)


def confirm(question: str) -> bool:
    return confirm_prompt(question)


def text_input(question: str, default: str | None = None) -> str:
    return text_input_prompt(question, default)
