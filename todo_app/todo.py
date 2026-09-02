"""Todo list module for managing tasks."""

from typing import List


class Todo:
    """A single todo item with a title and completion status."""
    
    def __init__(self, title: str) -> None:
        """Initialize a new todo item.
        
        Args:
            title: The title/description of the todo item.
        """
        self.title = title
        self.done = False


class TodoList:
    """A list of todo items with methods to manage them."""
    
    def __init__(self) -> None:
        """Initialize an empty todo list."""
        self._todos: List[Todo] = []
    
    def add(self, title: str) -> None:
        """Add a new todo item to the list.
        
        Args:
            title: The title/description of the todo item to add.
        """
        todo = Todo(title)
        self._todos.append(todo)
    
    def complete(self, index: int) -> None:
        """Mark a todo item as completed.
        
        Args:
            index: The index of the todo item to mark as done.
            
        Raises:
            ValueError: If the index is negative or out of range.
        """
        if index < 0 or index >= len(self._todos):
            raise ValueError(f"index {index} is out of range (0..{len(self._todos) - 1})")
        self._todos[index].done = True
    
    def list_all(self) -> List[Todo]:
        """Return all todo items in insertion order.
        
        Returns:
            A copy of the list of todo items.
        """
        return list(self._todos)
