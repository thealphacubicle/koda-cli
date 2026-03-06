"""Interactive REPL for koda CLI."""

try:
    import readline  # Enables up-arrow history when using input()

    readline.parse_and_bind("tab: complete")
except ImportError:
    pass  # readline not available on Windows

from core.banner import show_banner
from core.utils import CYAN, RED, RESET


def start_repl(commands: dict, version: str = "1.0.0"):
    """Run the interactive REPL loop."""
    show_banner()

    while True:
        try:
            raw = input(CYAN + "⚒  koda  > " + RESET).strip()
            if not raw:
                continue

            args = raw.split()
            command = args[0]
            rest = args[1:]

            if command in ("exit", "quit"):
                print("  See you later 👋")
                break

            if command in commands:
                try:
                    print()  # Newline after prompt line for clean output
                    commands[command](rest)
                except KeyboardInterrupt:
                    print()
                    continue
            else:
                print(f"  {RED}Unknown command: {command}. Type help to see all commands.{RESET}")

        except KeyboardInterrupt:
            print("\n  See you later 👋")
            break
