class Todo:
    """A todo item with a title and completion status."""
    
    def __init__(self, title):
        """Initialize a todo with the given title and done=False."""
        self.title = title
        self.done = False


class TodoList:
    """A list of todo items with methods to add, complete, and list todos."""
    
    def __init__(self):
        """Initialize an empty todo list."""
        self._todos = []
    
    def add(self, title):
        """Add a new todo with the given title."""
        todo = Todo(title)
        self._todos.append(todo)
    
    def list_all(self):
        """Return all todos in insertion order."""
        return self._todos
    
    def complete(self, index):
        """Mark the todo at the given index as complete.
        
        Raises ValueError if index is negative or out of range.
        """
        if index < 0 or index >= len(self._todos):
            raise ValueError("Index out of range")
        
        self._todos[index].done = True
