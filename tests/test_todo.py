import pytest


def _get_todo_classes():
    """Helper to safely import Todo classes, returning None if not available."""
    try:
        from todo_app.todo import Todo, TodoList
        return Todo, TodoList
    except (ImportError, AttributeError):
        return None, None


def test_todo_constructor_stores_title_and_defaults_done_false():
    """Test that Todo(title) stores the title and defaults done to False."""
    Todo, _ = _get_todo_classes()
    assert Todo is not None, 'todo_app.todo.Todo is not implemented yet'
    
    todo = Todo("Buy groceries")
    assert todo.title == "Buy groceries"
    assert todo.done is False


def test_todolist_add_and_list_all_insertion_order():
    """Test that TodoList.add appends todos and list_all returns them in insertion order."""
    _, TodoList = _get_todo_classes()
    assert TodoList is not None, 'todo_app.todo.TodoList is not implemented yet'
    
    todo_list = TodoList()
    todo_list.add("First task")
    todo_list.add("Second task")
    todo_list.add("Third task")
    
    todos = todo_list.list_all()
    assert len(todos) == 3
    assert todos[0].title == "First task"
    assert todos[1].title == "Second task"
    assert todos[2].title == "Third task"
    
    # Verify all are Todo instances with done defaulting to False
    for todo in todos:
        assert todo.done is False


def test_todolist_complete_marks_todo_done():
    """Test that TodoList.complete marks the todo at given index as done."""
    _, TodoList = _get_todo_classes()
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
    
    # Complete middle task
    todo_list.complete(1)
    
    # Verify only the specified task is marked done
    todos = todo_list.list_all()
    assert todos[0].done is False
    assert todos[1].done is True
    assert todos[2].done is False


def test_todolist_complete_raises_valueerror_for_out_of_range_positive_index():
    """Test that TodoList.complete raises ValueError for out-of-range positive index."""
    _, TodoList = _get_todo_classes()
    assert TodoList is not None, 'todo_app.todo.TodoList is not implemented yet'
    
    todo_list = TodoList()
    todo_list.add("Only task")
    
    # Index 1 is out of range for a list with only one item (index 0)
    with pytest.raises(ValueError):
        todo_list.complete(1)
    
    # Index 5 is way out of range
    with pytest.raises(ValueError):
        todo_list.complete(5)


def test_todolist_complete_raises_valueerror_for_negative_index():
    """Test that TodoList.complete raises ValueError for negative index."""
    _, TodoList = _get_todo_classes()
    assert TodoList is not None, 'todo_app.todo.TodoList is not implemented yet'
    
    todo_list = TodoList()
    todo_list.add("Task 1")
    todo_list.add("Task 2")
    
    # Negative indexes should raise ValueError
    with pytest.raises(ValueError):
        todo_list.complete(-1)
    
    with pytest.raises(ValueError):
        todo_list.complete(-2)
