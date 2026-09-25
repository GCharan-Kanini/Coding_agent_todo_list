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
