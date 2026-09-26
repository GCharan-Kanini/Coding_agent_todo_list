"""Command-line interface for the todo list application.

Provides a minimal 'add' command supporting both non-interactive and interactive
invocation. The main(argv) function is callable from tests and from a console
entrypoint.

Usage examples:
    main(['prog', 'add', 'My Task'])         # non-interactive
    main(['prog', 'add'])                    # interactive prompt
"""
from __future__ import annotations

import argparse
from typing import List, Optional

from src.domain import task as domain_task
from src.repository import in_memory_repository as repo
from src.cli import interactive_add


def _handle_add_args(title: Optional[str]) -> None:
    """Handle the add subcommand given an optional title.

    If title is provided and non-empty, validates and creates the task using
    the domain.create_task helper. If title is omitted (None), dispatch to the
    interactive flow which will prompt the user and call domain.create_task on
    success.
    """
    if title is None:
        # Run interactive flow; it will print its own messages
        interactive_add.run_interactive_add(repo)
        return

    # Non-interactive path: validate basic non-empty requirement and call domain
    if title.strip() == "":
        print("Task title must not be empty or whitespace-only")
        return

    try:
        domain_task.create_task(title)
        print(f"Task created: {title}")
    except ValueError as exc:
        print(str(exc))


def main(argv: Optional[List[str]] = None) -> None:
    """Parse arguments and dispatch commands.

    Args:
        argv: Optional list of command-line arguments (including program name)
            as provided to sys.argv. Tests call main([...]) directly to avoid
            touching the process global.
    """
    parser = argparse.ArgumentParser(prog="todo")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", nargs="?", help="Task title (optional; if omitted, prompts interactively)")

    args = parser.parse_args(argv[1:] if argv is not None else None)

    if args.command == "add":
        _handle_add_args(getattr(args, "title", None))
    else:
        parser.print_help()


if __name__ == "__main__":
    import sys

    main(sys.argv)
