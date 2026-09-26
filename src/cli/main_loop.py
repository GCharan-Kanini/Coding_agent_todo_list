"""Prompt-toolkit driven main loop for the todo CLI.

This module exposes run_main_loop(input_iter=None) which implements a simple
REPL reading commands from prompt_toolkit.prompt or from a provided input
iterator (for testing). Supported commands: add, view|list, mark-completed,
delete, exit, help.
"""
from __future__ import annotations

from typing import Iterable, Optional

import prompt_toolkit

from src.cli import cli


def _parse_command(token: str) -> tuple[str, list[str]]:
    parts = token.strip().split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def run_main_loop(input_iter: Optional[Iterable[str]] = None) -> None:
    """Run the interactive main loop.

    Args:
        input_iter: Optional iterator of input strings used for testing. When
            provided the function consumes inputs from it instead of calling
            prompt_toolkit.prompt.
    """
    iterator = iter(input_iter) if input_iter is not None else None

    while True:
        try:
            if iterator is not None:
                try:
                    token = next(iterator)
                except StopIteration:
                    return
            else:
                token = prompt_toolkit.prompt("todo> ")
        except KeyboardInterrupt:
            print("^C")
            continue

        cmd, args = _parse_command(token)
        if cmd in ("", "help"):
            print("Commands: add, view, list, mark-completed <index>, delete <index>, exit")
            continue

        if cmd == "exit":
            print("Goodbye")
            return

        try:
            if cmd == "add":
                # If args provided, treat as non-interactive add with title
                title = " ".join(args) if args else None
                cli._handle_add_args(title)
            elif cmd in ("view", "list"):
                cli.handle_view()
            elif cmd == "mark-completed":
                if not args:
                    print("Usage: mark-completed <index>")
                    continue
                try:
                    idx = int(args[0])
                except ValueError:
                    print("Please provide a numeric index.")
                    continue
                cli.handle_mark_completed(idx)
            elif cmd == "delete":
                if not args:
                    print("Usage: delete <index>")
                    continue
                try:
                    idx = int(args[0])
                except ValueError:
                    print("Please provide a numeric index.")
                    continue
                # Ask confirmation
                confirm = prompt_toolkit.prompt("Confirm delete? (y/N): ")
                if confirm.strip().lower().startswith("y"):
                    cli.handle_delete(idx, confirm=True)
                    print("Deleted")
                else:
                    print("Delete cancelled")
            else:
                print(f"Unknown command: {cmd}")
        except Exception as exc:  # pragma: no cover - defensive
            print(str(exc))
