"""Non-interactive argparse-based entrypoint for the todo CLI.

This module provides a main(argv) function suitable for tests and console
entrypoints. It supports the subcommands: add, view, mark-completed, delete.
"""
from __future__ import annotations

import argparse
from typing import List, Optional

from src.cli import cli


def main(argv: Optional[List[str]] = None) -> None:
    """Parse command-line arguments and dispatch to CLI handlers.

    This function is intended for non-interactive invocation from tests or a
    console entrypoint. It supports the subcommands: add, view, mark-completed,
    and delete. Inputs are validated and user-facing errors are reported via
    argparse's error mechanisms where appropriate.
    """
    parser = argparse.ArgumentParser(prog="todo-entry")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add")
    add_p.add_argument("title", nargs="?", help="Task title (optional)")

    subparsers.add_parser("view")

    mc = subparsers.add_parser("mark-completed")
    mc.add_argument("index", help="Zero-based task index")

    delete = subparsers.add_parser("delete")
    delete.add_argument("index", help="Zero-based task index")
    delete.add_argument("--yes", action="store_true", help="Confirm deletion")

    args = parser.parse_args(argv[1:] if argv is not None else None)

    if args.command == "add":
        title = getattr(args, "title", None)
        cli._handle_add_args(title)
    elif args.command == "view":
        cli.handle_view()
    elif args.command == "mark-completed":
        try:
            idx = int(args.index)
        except ValueError:
            parser.error("index must be an integer")
        cli.handle_mark_completed(idx)
    elif args.command == "delete":
        try:
            idx = int(args.index)
        except ValueError:
            parser.error("index must be an integer")
        cli.handle_delete(idx, confirm=bool(args.yes))
    else:
        parser.print_help()
