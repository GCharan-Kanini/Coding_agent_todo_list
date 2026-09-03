"""Task scheduler module for managing prioritized tasks with dependencies."""

from __future__ import annotations
import json
import datetime
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional, List, Dict, Set


class Priority(IntEnum):
    """Priority levels for tasks with ordering HIGH > MEDIUM > LOW."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class SchedulerError(Exception):
    """Base class for all scheduler-related errors."""
    pass


class DuplicateTaskError(SchedulerError, ValueError):
    """Raised when attempting to add a task with an existing ID."""
    pass


class UnknownTaskError(SchedulerError, KeyError):
    """Raised when referencing a task ID that doesn't exist."""
    pass


class CycleError(SchedulerError, ValueError):
    """Raised when a dependency would create a cycle."""
    pass


class BlockedTaskError(SchedulerError, ValueError):
    """Raised when attempting to complete a task with incomplete dependencies."""
    pass


@dataclass
class Task:
    """Represents a task with ID, title, priority, due date, and completion status."""
    task_id: str
    title: str
    priority: Priority
    due: Optional[datetime.date]
    done: bool = False


class TaskScheduler:
    """Manages tasks with priorities, dependencies, and scheduling."""
    
    def __init__(self) -> None:
        """Initialize an empty task scheduler."""
        self._tasks: Dict[str, Task] = {}
        self._dependencies: Dict[str, Set[str]] = {}
        self._insertion_order: List[str] = []
    
    def add(self, task_id: str, title: str, priority: Priority = Priority.MEDIUM, 
            due: Optional[datetime.date] = None) -> Task:
        """Add a new task to the scheduler.
        
        Args:
            task_id: Unique identifier for the task
            title: Task title (cannot be empty or whitespace-only)
            priority: Task priority (defaults to MEDIUM)
            due: Optional due date
            
        Returns:
            The created Task object
            
        Raises:
            DuplicateTaskError: If task_id already exists
            ValueError: If title is empty or whitespace-only
        """
        if task_id in self._tasks:
            raise DuplicateTaskError(f"Task with ID '{task_id}' already exists")
        
        if not title or title.isspace():
            raise ValueError(f"Title cannot be empty or whitespace-only: '{title}'")
        
        task = Task(task_id=task_id, title=title, priority=priority, due=due)
        self._tasks[task_id] = task
        self._dependencies[task_id] = set()
        self._insertion_order.append(task_id)
        
        return task
    
    def add_dependency(self, task_id: str, depends_on: str) -> None:
        """Add a dependency relationship between tasks.
        
        Args:
            task_id: ID of the task that depends on another
            depends_on: ID of the task that must be completed first
            
        Raises:
            UnknownTaskError: If either task ID doesn't exist
            CycleError: If the dependency would create a cycle
        """
        if task_id not in self._tasks:
            raise UnknownTaskError(f"Task '{task_id}' does not exist")
        
        if depends_on not in self._tasks:
            raise UnknownTaskError(f"Task '{depends_on}' does not exist")
        
        # Check for self-dependency
        if task_id == depends_on:
            raise CycleError(f"Task '{task_id}' cannot depend on itself")
        
        # Check for cycles by temporarily adding the dependency and checking reachability
        temp_deps = self._dependencies.copy()
        temp_deps[task_id].add(depends_on)
        
        if self._has_cycle(temp_deps, depends_on, task_id):
            raise CycleError(f"Adding dependency from '{task_id}' to '{depends_on}' would create a cycle")
        
        # No cycle detected, add the dependency
        self._dependencies[task_id].add(depends_on)
    
    def _has_cycle(self, deps: Dict[str, Set[str]], start: str, target: str) -> bool:
        """Check if there's a path from start to target in the dependency graph."""
        visited = set()
        stack = [start]
        
        while stack:
            current = stack.pop()
            if current == target:
                return True
            
            if current in visited:
                continue
            
            visited.add(current)
            stack.extend(deps.get(current, set()))
        
        return False
    
    def complete(self, task_id: str) -> None:
        """Mark a task as completed.
        
        Args:
            task_id: ID of the task to complete
            
        Raises:
            UnknownTaskError: If task_id doesn't exist
            BlockedTaskError: If the task has incomplete dependencies
        """
        if task_id not in self._tasks:
            raise UnknownTaskError(f"Task '{task_id}' does not exist")
        
        # Check if all dependencies are completed
        for dep_id in self._dependencies[task_id]:
            if not self._tasks[dep_id].done:
                raise BlockedTaskError(f"Cannot complete task '{task_id}' because dependency '{dep_id}' is not done")
        
        self._tasks[task_id].done = True
    
    def next_up(self, today: datetime.date) -> List[Task]:
        """Get pending tasks with completed dependencies, ordered by priority rules.
        
        Args:
            today: Current date for determining overdue tasks
            
        Returns:
            List of available tasks ordered by:
            1. Overdue tasks first
            2. Priority (HIGH > MEDIUM > LOW)
            3. Earlier due date
            4. Tasks with due dates before tasks without
            5. Insertion order
        """
        available_tasks = []
        
        for task_id, task in self._tasks.items():
            # Skip completed tasks
            if task.done:
                continue
            
            # Check if all dependencies are completed
            all_deps_done = all(self._tasks[dep_id].done for dep_id in self._dependencies[task_id])
            if all_deps_done:
                available_tasks.append(task)
        
        # Sort according to the priority rules
        def sort_key(task: Task) -> tuple:
            # 1. Overdue status (overdue tasks first)
            is_overdue = task.due is not None and task.due < today
            
            # 2. Priority (HIGH=3, MEDIUM=2, LOW=1, so negate for descending order)
            priority_order = -task.priority.value
            
            # 3. Due date (earlier first, None last)
            if task.due is None:
                due_order = (1, datetime.date.max)  # Put None dates last
            else:
                due_order = (0, task.due)
            
            # 4. Insertion order
            insertion_order = self._insertion_order.index(task.task_id)
            
            return (not is_overdue, priority_order, due_order, insertion_order)
        
        available_tasks.sort(key=sort_key)
        return available_tasks
    
    def to_json(self) -> str:
        """Serialize the scheduler state to JSON.
        
        Returns:
            JSON string representation of the scheduler
        """
        data = {
            'tasks': {},
            'dependencies': {},
            'insertion_order': self._insertion_order.copy()
        }
        
        # Serialize tasks
        for task_id, task in self._tasks.items():
            data['tasks'][task_id] = {
                'task_id': task.task_id,
                'title': task.title,
                'priority': task.priority.value,
                'due': task.due.isoformat() if task.due else None,
                'done': task.done
            }
        
        # Serialize dependencies
        for task_id, deps in self._dependencies.items():
            data['dependencies'][task_id] = list(deps)
        
        return json.dumps(data, sort_keys=True)
    
    @classmethod
    def from_json(cls, json_str: str) -> TaskScheduler:
        """Reconstruct a scheduler from JSON.
        
        Args:
            json_str: JSON string from to_json()
            
        Returns:
            New TaskScheduler instance with the same state
        """
        data = json.loads(json_str)
        
        scheduler = cls()
        scheduler._insertion_order = data['insertion_order']
        
        # Reconstruct tasks
        for task_id, task_data in data['tasks'].items():
            due_date = None
            if task_data['due']:
                due_date = datetime.date.fromisoformat(task_data['due'])
            
            task = Task(
                task_id=task_data['task_id'],
                title=task_data['title'],
                priority=Priority(task_data['priority']),
                due=due_date,
                done=task_data['done']
            )
            scheduler._tasks[task_id] = task
        
        # Reconstruct dependencies
        for task_id, deps in data['dependencies'].items():
            scheduler._dependencies[task_id] = set(deps)
        
        return scheduler