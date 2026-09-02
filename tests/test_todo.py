import pytest

def get_todo_class():
    """Helper to safely import Todo class."""
    try:
        from todo_app.todo import Todo
        return Todo
    except (ImportError, AttributeError):
        return None

def test_todo_initialization():
    """Test that Todo class stores title and defaults done to False."""
    Todo = get_todo_class()
    assert Todo is not None, 'todo_app.todo.Todo is not implemented yet'
    
    # Test with a simple title
    todo = Todo("Buy groceries")
    assert todo.title == "Buy groceries"
    assert todo.done is False
    
    # Test with different title
    todo2 = Todo("Walk the dog")
    assert todo2.title == "Walk the dog"
    assert todo2.done is False
    
    # Test with empty title
    todo3 = Todo("")
    assert todo3.title == ""
    assert todo3.done is False
