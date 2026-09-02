import pytest


def get_todo_classes():
    """Helper to safely import Todo classes, returns None if not implemented."""
    try:
        from todo_app.todo import Todo, TodoList
        return Todo, TodoList
    except (ImportError, AttributeError):
        return None, None


def test_todo_creation_with_title_and_default_done():
    """Test that Todo stores title and defaults done to False."""
    Todo, _ = get_todo_classes()
    assert Todo is not None, 'todo_app.todo.Todo is not implemented yet'
    
    todo = Todo("Buy groceries")
    assert todo.title == "Buy groceries"
    assert todo.done is False


def test_todolist_add_and_list_all():
    """Test that TodoList can add todos and list them in insertion order."""
    Todo, TodoList = get_todo_classes()
    assert TodoList is not None, 'todo_app.todo.TodoList is not implemented yet'
    
    todo_list = TodoList()
    
    # Add multiple todos
    todo_list.add("First task")
    todo_list.add("Second task")
    todo_list.add("Third task")
    
    # Get all todos
    todos = todo_list.list_all()
    
    # Verify insertion order and content
    assert len(todos) == 3
    assert todos[0].title == "First task"
    assert todos[1].title == "Second task"
    assert todos[2].title == "Third task"
    
    # Verify all are Todo instances with default done=False
    for todo in todos:
        assert hasattr(todo, 'title')
        assert hasattr(todo, 'done')
        assert todo.done is False


def test_todolist_complete_by_index():
    """Test that TodoList can mark todos as complete by index."""
    Todo, TodoList = get_todo_classes()
    assert TodoList is not None, 'todo_app.todo.TodoList is not implemented yet'
    
    todo_list = TodoList()
    todo_list.add("Task 1")
    todo_list.add("Task 2")
    todo_list.add("Task 3")
    
    # Initially all should be not done
    todos = todo_list.list_all()
    assert todos[0].done is False
    assert todos[1].done is False
    assert todos[2].done is False
    
    # Complete the second task (index 1)
    todo_list.complete(1)
    
    # Verify only the second task is marked as done
    todos = todo_list.list_all()
    assert todos[0].done is False
    assert todos[1].done is True
    assert todos[2].done is False
    
    # Complete the first task (index 0)
    todo_list.complete(0)
    
    # Verify both first and second tasks are done
    todos = todo_list.list_all()
    assert todos[0].done is True
    assert todos[1].done is True
    assert todos[2].done is False


def test_todolist_complete_invalid_index_raises_valueerror():
    """Test that TodoList raises ValueError for invalid indexes in complete method."""
    Todo, TodoList = get_todo_classes()
    assert TodoList is not None, 'todo_app.todo.TodoList is not implemented yet'
    
    todo_list = TodoList()
    todo_list.add("Task 1")
    todo_list.add("Task 2")
    
    # Test negative index raises ValueError
    with pytest.raises(ValueError):
        todo_list.complete(-1)
    
    # Test index equal to length raises ValueError
    with pytest.raises(ValueError):
        todo_list.complete(2)
    
    # Test index greater than length raises ValueError
    with pytest.raises(ValueError):
        todo_list.complete(5)
    
    # Test on empty list
    empty_list = TodoList()
    with pytest.raises(ValueError):
        empty_list.complete(0)
    
    # Verify valid indexes still work
    todo_list.complete(0)  # Should not raise
    todo_list.complete(1)  # Should not raise
