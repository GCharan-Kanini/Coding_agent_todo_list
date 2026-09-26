"""Process-local in-memory repository for Task objects.

This module maintains a module-scoped list that lives only for the duration of
the running Python process. It provides functions to inspect the current list
and an internal append helper used by src.domain.task.create_task.

Notes:
- The repository does not persist to disk or external storage.
- list_tasks() returns a shallow copy of the internal list so callers may
  mutate the returned list without affecting repository state.
"""
from __future__ import annotations

from typing import List

from src.domain.task import Task

# Module-private in-memory storage
_TASKS: List[Task] = []


def _append_task(task: Task) -> None:
    """Append a validated Task to the in-memory list.

    This private helper is intentionally minimal; validation is expected to
    happen at the domain boundary (src.domain.task.create_task).
    """
    _TASKS.append(task)


def list_tasks() -> List[Task]:
    """Return a shallow copy of the current in-memory task list.

    Returns:
        A list containing the Task instances currently stored. Mutating the
        returned list does not affect repository internal state.
    """
    return list(_TASKS)


def clear_tasks_for_testing() -> None:
    """Clear repository contents. Intended for tests; not part of public API.

    This helper exists to make tests deterministic if they choose to call it.
    Tests in this repository prefer importlib.reload to reset state, so this
    function is optional.
    """
    _TASKS.clear()


def update_task_status(index: int, status: str) -> None:
    """Update the status of the task at the given zero-based index.

    Args:
        index: Zero-based index of the task to update.
        status: New status string; must be one of the domain-allowed statuses.

    Raises:
        IndexError: If index is out of range.
        ValueError: If status is not allowed.
    """
    from src.domain.task import ALLOWED_STATUSES

    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status '{status}'. Allowed: {ALLOWED_STATUSES}")

    try:
        _TASKS[index].status = status
    except IndexError:
        raise IndexError(f"index {index} is out of range (0..{len(_TASKS) - 1})")


def remove_task(index: int) -> None:
    """Remove the task at the given zero-based index from the repository.

    Args:
        index: Zero-based index of the task to remove.

    Raises:
        IndexError: If index is out of range.
    """
    try:
        del _TASKS[index]
    except IndexError:
        raise IndexError(f"index {index} is out of range (0..{len(_TASKS) - 1})")
