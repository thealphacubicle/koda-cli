"""Shared ANSI styling and terminal utilities for forge CLI."""

import sys
import time
import threading
import itertools

# ANSI escape codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"

# Spinner frames (braille pattern)
SPINNER_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"


def typewrite(text: str, delay: float = 0.02) -> None:
    """Print text character by character with a typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def typewrite_no_newline(text: str, delay: float = 0.02) -> None:
    """Print text character by character without trailing newline."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.flush()


def divider(char: str = "─", width: int = 60) -> str:
    """Return a divider line."""
    return DIM + (char * width) + RESET


def print_divider(char: str = "─", width: int = 60) -> None:
    """Print a divider line."""
    sys.stdout.write(divider(char, width) + "\n")
    sys.stdout.flush()


def spinner_context(message: str):
    """
    Context manager that shows a spinner while the block runs.
    Uses a background thread for the spinner animation.
    """
    class SpinnerContext:
        def __init__(self, msg):
            self.msg = msg
            self.done = False
            self.thread = None

        def __enter__(self):
            self.done = False
            frames = itertools.cycle(SPINNER_FRAMES)

            def spin():
                while not self.done:
                    frame = next(frames)
                    sys.stdout.write(f"\r{CYAN}{frame}{RESET} {self.msg}   ")
                    sys.stdout.flush()
                    time.sleep(0.1)
                sys.stdout.write(f"\r{GREEN}✓{RESET} {self.msg}   \n")
                sys.stdout.flush()

            self.thread = threading.Thread(target=spin)
            self.thread.start()
            return self

        def __exit__(self, *args):
            self.done = True
            if self.thread:
                self.thread.join()
            return False

    return SpinnerContext(message)


def run_with_spinner(message: str, func, *args, **kwargs):
    """Run a function while showing a spinner. Returns the function's result."""
    result = [None]
    exception = [None]

    def run():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=run)
    frames = itertools.cycle(SPINNER_FRAMES)
    thread.start()

    while thread.is_alive():
        frame = next(frames)
        sys.stdout.write(f"\r{CYAN}{frame}{RESET} {message}   ")
        sys.stdout.flush()
        time.sleep(0.1)

    thread.join()
    sys.stdout.write(f"\r{GREEN}✓{RESET} {message}   \n")
    sys.stdout.flush()

    if exception[0]:
        raise exception[0]
    return result[0]
