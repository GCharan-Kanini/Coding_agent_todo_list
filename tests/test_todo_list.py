import pytest

def get_todo_classes():
    """Helper to safely import Todo and TodoList classes."""
    try:
        from todo_app.todo import Todo, TodoList
        return Todo, TodoList
    except (ImportError, AttributeError):
        return None, None

def test_add_and_list_todos():
    """Test that TodoList can add todos and list them in insertion order."""
    Todo, TodoList = get_todo_classes()
    assert TodoList is not None, 'todo_app.todo.TodoList is not implemented yet'
    assert Todo is not None, 'todo_app.todo.Todo is not implemented yet'
    
    todo_list = TodoList()
    
    # Initially empty
    todos = todo_list.list_all()
    assert todos == []
    
    # Add first todo
    todo_list.add("Buy groceries")
    todos = todo_list.list_all()
    assert len(todos) == 1
    assert todos[0].title == "Buy groceries"
    assert todos[0].done is False
    
    # Add second todo
    todo_list.add("Walk the dog")
    todos = todo_list.list_all()
    assert len(todos) == 2
    assert todos[0].title == "Buy groceries"
    assert todos[1].title == "Walk the dog"
    
    # Add third todo to verify insertion order
    todo_list.add("Do laundry")
    todos = todo_list.list_all()
    assert len(todos) == 3
    assert todos[0].title == "Buy groceries"
    assert todos[1].title == "Walk the dog"
    assert todos[2].title == "Do laundry"
    
    # Verify all are not done by default
    for todo in todos:
        assert todo.done is False

def test_complete_todo_by_index():
    """Test that TodoList.complete() marks todo at specified index as done."""
    Todo, TodoList = get_todo_classes()
    assert TodoList is not None, 'todo_app.todo.TodoList is not implemented yet'
    assert Todo is not None, 'todo_app.todo.Todo is not implemented yet'
    
    todo_list = TodoList()
    todo_list.add("Buy groceries")
    todo_list.add("Walk the dog")
    todo_list.add("Do laundry")
    
    # Complete first todo (index 0)
    todo_list.complete(0)
    todos = todo_list.list_all()
    assert todos[0].done is True
    assert todos[1].done is False
    assert todos[2].done is False
    
    # Complete third todo (index 2)
    todo_list.complete(2)
    todos = todo_list.list_all()
    assert todos[0].done is True
    assert todos[1].done is False
    assert todos[2].done is True
    
    # Complete middle todo (index 1)
    todo_list.complete(1)
    todos = todo_list.list_all()
    assert todos[0].done is True
    assert todos[1].done is True
    assert todos[2].done is True

def test_complete_todo_invalid_index():
    """Test that TodoList.complete() raises ValueError for out-of-range indexes."""
    Todo, TodoList = get_todo_classes()
    assert TodoList is not None, 'todo_app.todo.TodoList is not implemented yet'
    assert Todo is not None, 'todo_app.todo.Todo is not implemented yet'
    
    todo_list = TodoList()
    
    # Test with empty list
    with pytest.raises(ValueError):
        todo_list.complete(0)
    
    with pytest.raises(ValueError):
        todo_list.complete(-1)
    
    # Add some todos
    todo_list.add("Buy groceries")
    todo_list.add("Walk the dog")
    
    # Test negative indexes (should be out of range)
    with pytest.raises(ValueError):
        todo_list.complete(-1)
    
    with pytest.raises(ValueError):
        todo_list.complete(-2)
    
    # Test index equal to length (out of range)
    with pytest.raises(ValueError):
        todo_list.complete(2)
    
    # Test index greater than length
    with pytest.raises(ValueError):
        todo_list.complete(5)
    
    # Verify valid indexes still work
    todo_list.complete(0)  # Should not raise
    todo_list.complete(1)  # Should not raise
