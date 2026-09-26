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


def handle_view() -> None:
    """Handle the view command by printing the in-memory task list.

    This function is intentionally read-only: it retrieves the current
    in-memory tasks from the repository and renders them to stdout. It does
    not perform any file or network I/O and does not modify repository state.

    Behaviour:
    - When one or more tasks exist: prints exactly one line per task in the
      format "<index>. <title> - <status>" where index is 1-based and status is
      shown verbatim ("Pending" or "Completed").
    - When no tasks exist: prints the clear message "No tasks found.".
    """
    tasks = repo.list_tasks()

    if not tasks:
        print("No tasks found.")
        return

    for idx, task in enumerate(tasks, start=1):
        # Print index, title and status verbatim per acceptance criteria
        print(f"{idx}. {task.title} - {task.status}")


def handle_mark_completed(index: int) -> None:
    """Mark the task at zero-based index as Completed.

    The handler validates the provided index (must be an int within range)
    and updates repository state. On invalid input a ValueError is raised and
    repository state is not modified.
    """
    # Validate input type
    if not isinstance(index, int):
        raise ValueError(f"Invalid index: {index!r}")

    tasks = repo.list_tasks()
    if index < 0 or index >= len(tasks):
        raise ValueError(f"index {index} is out of range (0..{len(tasks) - 1})")

    # Update status via repository helper
    repo.update_task_status(index, "Completed")


def handle_delete(index: int, confirm: bool = False) -> None:
    """Delete the task at zero-based index if confirmed.

    Args:
        index: Zero-based index of the task to delete.
        confirm: When True perform deletion; when False do nothing.

    Raises:
        ValueError: If index is not an int or out of range.
    """
    if not isinstance(index, int):
        raise ValueError(f"Invalid index: {index!r}")

    tasks = repo.list_tasks()
    if index < 0 or index >= len(tasks):
        raise ValueError(f"index {index} is out of range (0..{len(tasks) - 1})")

    if confirm:
        repo.remove_task(index)


def dispatch_command(command: str, params: dict) -> None:
    """Dispatch a simple command to the corresponding handler.

    This helper is used by tests to exercise dispatch behaviour without
    invoking the interactive main loop.
    """
    if command == "add":
        title = params.get("title")
        _handle_add_args(title)
    elif command in ("view", "list"):
        handle_view()
    elif command == "mark-completed":
        idx = params.get("index")
        handle_mark_completed(idx)
    elif command == "delete":
        idx = params.get("index")
        confirm = bool(params.get("confirm", False))
        handle_delete(idx, confirm=confirm)
    elif command == "exit":
        # No-op for dispatch; callers handle loop termination
        return
    else:
        raise ValueError(f"unknown command: {command}")


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

    # View subcommand: show current in-memory tasks without modifying them
    view_parser = subparsers.add_parser("view", help="View current tasks")

    args = parser.parse_args(argv[1:] if argv is not None else None)

    if args.command == "add":
        _handle_add_args(getattr(args, "title", None))
    elif args.command == "view":
        handle_view()
    else:
        parser.print_help()


if __name__ == "__main__":
    import sys

    main(sys.argv)
