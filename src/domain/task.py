"""Task domain model and factory helpers.

This module exposes a simple Task dataclass and a create_task(...) helper
that validates input according to the project's domain rules:

- Titles must not be empty or whitespace-only. All characters (including
  leading/trailing whitespace and special characters) are preserved exactly.
- Status must be exactly the string "Pending" or "Completed". If status
  is omitted, it defaults to "Pending".

The create_task function appends the created Task into the process-local
in-memory repository in src.repository.in_memory_repository. The repository
is process-local and non-persistent.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


ALLOWED_STATUSES = ("Pending", "Completed")


@dataclass
class Task:
    """A task record stored in-process for the lifetime of the program run.

    Attributes:
        title: The task title. Preserved exactly as provided by callers.
        status: Either "Pending" or "Completed".
    """

    title: str
    status: str


def create_task(title: str, status: Optional[str] = None) -> Task:
    """Validate inputs, create a Task and append it to the in-memory repository.

    Args:
        title: The task title. Must not be empty or whitespace-only. Characters
            are preserved exactly; no trimming is performed.
        status: Optional explicit status. When omitted, defaults to "Pending".

    Returns:
        The created Task instance (the same object stored in the repository).

    Raises:
        ValueError: when validation fails for title or status.
    """
    # Title validation: must contain at least one non-whitespace character
    if title is None or title.strip() == "":
        raise ValueError(f"Task title must not be empty or whitespace-only: {repr(title)}")

    if status is None:
        status = "Pending"

    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Allowed: {ALLOWED_STATUSES}")

    task = Task(title=title, status=status)

    # Append to the process-local repository. Import locally to avoid
    # import-time cycles and to ensure reload() semantics in tests work.
    from src.repository import in_memory_repository as _repo

    _repo._append_task(task)

    return task
