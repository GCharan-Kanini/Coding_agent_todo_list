import pytest
from todo_app.todo import Todo, TodoList


def test_todo_constructor_stores_title_and_defaults_done():
    """Test that Todo constructor stores title and defaults done to False."""
    todo = Todo("Buy groceries")
    assert todo.title == "Buy groceries"
    assert todo.done is False


def test_todolist_add_and_list_all_insertion_order():
    """Test that TodoList.add() appends new Todo and list_all() returns in insertion order."""
    todo_list = TodoList()
    
    # Add multiple todos
    todo_list.add("First task")
    todo_list.add("Second task")
    todo_list.add("Third task")
    
    # Get all todos
    todos = todo_list.list_all()
    
    # Verify insertion order
    assert len(todos) == 3
    assert todos[0].title == "First task"
    assert todos[1].title == "Second task"
    assert todos[2].title == "Third task"
    
    # Verify all are Todo instances with default done=False
    for todo in todos:
        assert isinstance(todo, Todo)
        assert todo.done is False


def test_todolist_complete_marks_todo_done():
    """Test that TodoList.complete() marks todo at given index as done."""
    todo_list = TodoList()
    todo_list.add("Task 1")
    todo_list.add("Task 2")
    todo_list.add("Task 3")
    
    # Complete the second task (index 1)
    todo_list.complete(1)
    
    todos = todo_list.list_all()
    assert todos[0].done is False  # First task still not done
    assert todos[1].done is True   # Second task marked as done
    assert todos[2].done is False  # Third task still not done


def test_todolist_complete_raises_valueerror_for_positive_out_of_range():
    """Test that TodoList.complete() raises ValueError for out-of-range positive index."""
    todo_list = TodoList()
    todo_list.add("Only task")
    
    # Try to complete index 1 when only index 0 exists
    with pytest.raises(ValueError):
        todo_list.complete(1)
    
    # Try to complete index 5 when only index 0 exists
    with pytest.raises(ValueError):
        todo_list.complete(5)


def test_todolist_complete_raises_valueerror_for_negative_index():
    """Test that TodoList.complete() raises ValueError for negative index."""
    todo_list = TodoList()
    todo_list.add("Task 1")
    todo_list.add("Task 2")
    
    # Try to complete with negative index
    with pytest.raises(ValueError):
        todo_list.complete(-1)
    
    with pytest.raises(ValueError):
        todo_list.complete(-2)


def test_todolist_complete_raises_valueerror_for_empty_list():
    """Test that TodoList.complete() raises ValueError for index on empty list."""
    todo_list = TodoList()
    
    # Try to complete index 0 on empty list
    with pytest.raises(ValueError):
        todo_list.complete(0)
