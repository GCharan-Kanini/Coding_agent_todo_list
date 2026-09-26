"""Interactive add flow using prompt_toolkit.

This module provides a run_interactive_add(repo) function that prompts the
user for a task title using prompt_toolkit.prompt, validates the input (rejects
empty or whitespace-only titles), allows retry on invalid input, supports
cancellation via KeyboardInterrupt, and calls the domain create_task(...) API
which in turn appends the validated Task to the provided repository module.

The interactive flow intentionally avoids reimplementing domain validation for
status values and relies on src.domain.task.create_task for final validation
and repository appending behaviour.
"""
from __future__ import annotations

from typing import Optional, Any

import prompt_toolkit


def prompt_for_title() -> Optional[str]:
    """Prompt the user for a task title.

    Returns the entered title string, or None if the user cancelled the prompt
    (KeyboardInterrupt).
    """
    try:
        # prompt_toolkit.prompt is monkeypatched in tests; pass a helpful prompt
        # string but don't rely on any advanced features.
        title = prompt_toolkit.prompt("Task title: ")
    except KeyboardInterrupt:
        return None

    return title


def run_interactive_add(repo_module: Any) -> None:
    """Run the interactive add flow.

    The function repeatedly prompts the user for a non-empty title. If the
    user cancels (KeyboardInterrupt) the flow prints a cancellation message and
    returns without creating a task. On valid input the function calls the
    domain create_task(...) helper which appends the created Task to the
    in-memory repository.

    Args:
        repo_module: The repository module (e.g., src.repository.in_memory_repository)
            passed by callers and also used indirectly by src.domain.task.create_task.

    Behavior:
        - Prints validation and error messages to stdout.
        - Does not raise on user cancellation; returns after printing feedback.
    """
    from src.domain import task as domain_task

    while True:
        title = prompt_for_title()

        if title is None:
            # user cancelled
            print("Add cancelled by user")
            return

        if title.strip() == "":
            # Mirror the domain validation message so tests can assert on it
            print("Task title must not be empty or whitespace-only")
            continue

        try:
            # Domain-level create_task performs validation and appends to repo
            domain_task.create_task(title)
            print(f"Task created: {title}")
            return
        except ValueError as exc:
            # Show validation errors coming from the domain layer and allow retry
            print(str(exc))
            continue
