"""Task scheduling primitives for todo_app.

This module provides an in-memory task scheduler that supports priorities,
due dates, dependency constraints, cycle prevention, and JSON round-tripping.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import IntEnum
import json
from typing import Any


class SchedulerError(Exception):
    """Base class for all scheduler-related errors."""


class DuplicateTaskError(SchedulerError, ValueError):
    """Raised when adding a task whose identifier already exists."""


class UnknownTaskError(SchedulerError, KeyError):
    """Raised when a referenced task identifier does not exist."""


class CycleError(SchedulerError, ValueError):
    """Raised when a dependency addition would create a cycle."""


class BlockedTaskError(SchedulerError, ValueError):
    """Raised when trying to complete a task with pending dependencies."""


class Priority(IntEnum):
    """Priority levels ordered from LOW to HIGH."""

    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass(slots=True)
class Task:
    """A scheduled task.

    Attributes:
        task_id: Stable identifier for the task.
        title: Human readable title.
        priority: Task urgency represented by :class:`Priority`.
        due: Optional due date.
        done: Completion flag.
    """

    task_id: str
    title: str
    priority: Priority
    due: date | None = None
    done: bool = False


class TaskScheduler:
    """Manage tasks, dependencies, completion, ordering, and serialization."""

    def __init__(self) -> None:
        """Initialize an empty scheduler."""
        self._tasks: dict[str, Task] = {}
        self._dependencies: dict[str, set[str]] = {}

    def add(
        self,
        task_id: str,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due: date | None = None,
    ) -> Task:
        """Add a task and return it.

        Raises:
            DuplicateTaskError: If ``task_id`` already exists.
            ValueError: If ``title`` is empty or whitespace-only.
            TypeError: If ``due`` is neither ``None`` nor ``datetime.date``.
        """
        if task_id in self._tasks:
            raise DuplicateTaskError(f"task_id {task_id!r} already exists")

        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"title {title!r} must contain non-whitespace characters")

        if due is not None and not isinstance(due, date):
            raise TypeError(f"due {due!r} must be a datetime.date or None")

        task_priority = self._coerce_priority(priority)
        task = Task(task_id=task_id, title=title, priority=task_priority, due=due)
        self._tasks[task_id] = task
        self._dependencies[task_id] = set()
        return task

    def add_dependency(self, task_id: str, depends_on: str) -> None:
        """Record that ``task_id`` depends on ``depends_on``.

        Raises:
            UnknownTaskError: If either task identifier is unknown.
            CycleError: If the dependency would introduce a cycle.
        """
        self._require_known_task(task_id)
        self._require_known_task(depends_on)

        if task_id == depends_on:
            raise CycleError(f"dependency from {task_id!r} to itself would create a cycle")

        if task_id in self._dependencies[task_id]:
            return

        if self._path_exists(start=depends_on, target=task_id):
            raise CycleError(
                f"dependency {task_id!r} -> {depends_on!r} would create a cycle"
            )

        self._dependencies[task_id].add(depends_on)

    def complete(self, task_id: str) -> None:
        """Mark a task as complete.

        Raises:
            UnknownTaskError: If ``task_id`` is unknown.
            BlockedTaskError: If any dependency is still pending.
        """
        self._require_known_task(task_id)
        blocked_by = [dep for dep in self._dependencies[task_id] if not self._tasks[dep].done]
        if blocked_by:
            raise BlockedTaskError(
                f"task {task_id!r} is blocked by pending dependencies {blocked_by!r}"
            )

        self._tasks[task_id].done = True

    def next_up(self, today: date) -> list[Task]:
        """Return completable pending tasks ordered by scheduler priority rules."""
        if not isinstance(today, date):
            raise TypeError(f"today {today!r} must be a datetime.date")

        candidates = [
            task
            for task_id, task in self._tasks.items()
            if not task.done and self._dependencies_done(task_id)
        ]

        return sorted(candidates, key=lambda task: self._sort_key(task, today))

    def to_json(self) -> str:
        """Serialize scheduler state to a JSON string."""
        payload = {
            "tasks": [
                {
                    "task_id": task.task_id,
                    "title": task.title,
                    "priority": task.priority.name,
                    "due": task.due.isoformat() if task.due is not None else None,
                    "done": task.done,
                }
                for task in self._tasks.values()
            ],
            "dependencies": {
                task_id: sorted(depends_on)
                for task_id, depends_on in self._dependencies.items()
            },
        }
        return json.dumps(payload, separators=(",", ":"))

    @classmethod
    def from_json(cls, text: str) -> TaskScheduler:
        """Build a scheduler from :meth:`to_json` output."""
        raw = json.loads(text)
        if not isinstance(raw, dict):
            raise ValueError(f"scheduler JSON must decode to an object, got {type(raw).__name__}")

        tasks_data = raw.get("tasks")
        dependencies_data = raw.get("dependencies")
        if not isinstance(tasks_data, list):
            raise ValueError("scheduler JSON field 'tasks' must be a list")
        if not isinstance(dependencies_data, dict):
            raise ValueError("scheduler JSON field 'dependencies' must be an object")

        scheduler = cls()

        for item in tasks_data:
            if not isinstance(item, dict):
                raise ValueError(f"task entry {item!r} must be an object")

            task_id = item.get("task_id")
            title = item.get("title")
            priority_name = item.get("priority")
            due_text = item.get("due")
            done = item.get("done", False)

            if not isinstance(task_id, str):
                raise ValueError(f"task_id {task_id!r} must be a string")
            if not isinstance(title, str):
                raise ValueError(f"title {title!r} must be a string")
            if not isinstance(priority_name, str):
                raise ValueError(f"priority {priority_name!r} must be a string")
            if due_text is not None and not isinstance(due_text, str):
                raise ValueError(f"due {due_text!r} must be an ISO date string or None")
            if not isinstance(done, bool):
                raise ValueError(f"done {done!r} must be a bool")

            try:
                priority = Priority[priority_name]
            except KeyError as exc:
                raise ValueError(f"unknown priority {priority_name!r}") from exc

            due = date.fromisoformat(due_text) if due_text is not None else None
            created = scheduler.add(task_id=task_id, title=title, priority=priority, due=due)
            created.done = done

        for task_id, depends_list in dependencies_data.items():
            if not isinstance(task_id, str):
                raise ValueError(f"dependency key {task_id!r} must be a string")
            if not isinstance(depends_list, list):
                raise ValueError(
                    f"dependency list for task {task_id!r} must be a list, got {type(depends_list).__name__}"
                )
            for dependency in depends_list:
                if not isinstance(dependency, str):
                    raise ValueError(
                        f"dependency {dependency!r} for task {task_id!r} must be a string"
                    )
                scheduler.add_dependency(task_id, dependency)

        return scheduler

    def _coerce_priority(self, priority: Priority) -> Priority:
        """Return a Priority instance from a priority-like value."""
        try:
            return priority if isinstance(priority, Priority) else Priority(priority)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"priority {priority!r} is invalid") from exc

    def _require_known_task(self, task_id: str) -> None:
        """Raise ``UnknownTaskError`` when ``task_id`` does not exist."""
        if task_id not in self._tasks:
            raise UnknownTaskError(f"unknown task_id {task_id!r}")

    def _dependencies_done(self, task_id: str) -> bool:
        """Return whether all dependencies of ``task_id`` are completed."""
        return all(self._tasks[dependency].done for dependency in self._dependencies[task_id])

    def _path_exists(self, start: str, target: str) -> bool:
        """Return whether a dependency path exists from ``start`` to ``target``."""
        stack = [start]
        seen: set[str] = set()

        while stack:
            current = stack.pop()
            if current == target:
                return True
            if current in seen:
                continue
            seen.add(current)
            stack.extend(self._dependencies[current])

        return False

    def _sort_key(self, task: Task, today: date) -> tuple[int, int, date, int]:
        """Build a stable sorting key for ``next_up`` ordering."""
        due = task.due

        if due is None:
            due_bucket = 3
            due_for_sort = date.max
        elif due < today:
            due_bucket = 0
            due_for_sort = due
        elif due == today:
            due_bucket = 1
            due_for_sort = due
        else:
            due_bucket = 2
            due_for_sort = due

        insertion_order = list(self._tasks).index(task.task_id)
        return (due_bucket, -int(task.priority), due_for_sort, insertion_order)
