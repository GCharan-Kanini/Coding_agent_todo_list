import pytest
import datetime
import json


def get_scheduler_module():
    """Helper to safely import scheduler module."""
    try:
        import todo_app.scheduler
        return todo_app.scheduler
    except (ImportError, AttributeError):
        return None


def test_priority_enum_members_and_ordering():
    """Test that Priority enum exists with correct members and ordering."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    Priority = getattr(scheduler, 'Priority', None)
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    # Check enum members exist
    assert hasattr(Priority, 'LOW'), 'Priority.LOW is not implemented'
    assert hasattr(Priority, 'MEDIUM'), 'Priority.MEDIUM is not implemented'
    assert hasattr(Priority, 'HIGH'), 'Priority.HIGH is not implemented'
    
    # Check ordering
    assert Priority.HIGH > Priority.MEDIUM, 'Priority.HIGH should be greater than Priority.MEDIUM'
    assert Priority.MEDIUM > Priority.LOW, 'Priority.MEDIUM should be greater than Priority.LOW'
    assert Priority.HIGH > Priority.LOW, 'Priority.HIGH should be greater than Priority.LOW'


def test_add_task_returns_correct_attributes():
    """Test that TaskScheduler.add returns Task with correct attributes."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    Priority = getattr(scheduler, 'Priority', None)
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    ts = TaskScheduler()
    due_date = datetime.date(2024, 1, 15)
    
    # Test with all parameters
    task = ts.add('task1', 'Test Task', Priority.HIGH, due_date)
    
    assert hasattr(task, 'task_id'), 'Task should have task_id attribute'
    assert hasattr(task, 'title'), 'Task should have title attribute'
    assert hasattr(task, 'priority'), 'Task should have priority attribute'
    assert hasattr(task, 'due'), 'Task should have due attribute'
    assert hasattr(task, 'done'), 'Task should have done attribute'
    
    assert task.task_id == 'task1', 'Task task_id should match input'
    assert task.title == 'Test Task', 'Task title should match input'
    assert task.priority == Priority.HIGH, 'Task priority should match input'
    assert task.due == due_date, 'Task due date should match input'
    assert task.done is False, 'Task done should default to False'
    
    # Test with defaults
    task2 = ts.add('task2', 'Default Task')
    assert task2.priority == Priority.MEDIUM, 'Default priority should be MEDIUM'
    assert task2.due is None, 'Default due should be None'
    assert task2.done is False, 'Default done should be False'


def test_add_duplicate_task_raises_error():
    """Test that adding duplicate task_id raises DuplicateTaskError."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    DuplicateTaskError = getattr(scheduler, 'DuplicateTaskError', None)
    assert DuplicateTaskError is not None, 'DuplicateTaskError is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'First Task')
    
    with pytest.raises(DuplicateTaskError):
        ts.add('task1', 'Duplicate Task')


def test_add_empty_title_raises_error():
    """Test that empty or whitespace-only title raises ValueError."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    ts = TaskScheduler()
    
    # Test empty string
    with pytest.raises(ValueError):
        ts.add('task1', '')
    
    # Test whitespace only
    with pytest.raises(ValueError):
        ts.add('task2', '   ')
    
    # Test tab and newline
    with pytest.raises(ValueError):
        ts.add('task3', '\t\n  ')


def test_add_dependency_success():
    """Test that add_dependency successfully records dependencies."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'First Task')
    ts.add('task2', 'Second Task')
    
    # Should not raise any exception
    ts.add_dependency('task2', 'task1')
    
    # Verify dependency is recorded by checking next_up behavior
    today = datetime.date.today()
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    # task2 should not be in next_up since task1 is not done
    assert 'task1' in task_ids, 'task1 should be available'
    assert 'task2' not in task_ids, 'task2 should be blocked by dependency'


def test_add_dependency_unknown_task_error():
    """Test that add_dependency raises UnknownTaskError for unknown ids."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    UnknownTaskError = getattr(scheduler, 'UnknownTaskError', None)
    assert UnknownTaskError is not None, 'UnknownTaskError is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'Existing Task')
    
    # Unknown task_id
    with pytest.raises(UnknownTaskError):
        ts.add_dependency('unknown', 'task1')
    
    # Unknown depends_on
    with pytest.raises(UnknownTaskError):
        ts.add_dependency('task1', 'unknown')
    
    # Both unknown
    with pytest.raises(UnknownTaskError):
        ts.add_dependency('unknown1', 'unknown2')


def test_add_dependency_cycle_prevention():
    """Test that add_dependency prevents cycles and leaves scheduler unchanged."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    CycleError = getattr(scheduler, 'CycleError', None)
    assert CycleError is not None, 'CycleError is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'First Task')
    ts.add('task2', 'Second Task')
    ts.add('task3', 'Third Task')
    
    # Self-dependency
    with pytest.raises(CycleError):
        ts.add_dependency('task1', 'task1')
    
    # Create a valid dependency chain
    ts.add_dependency('task2', 'task1')
    ts.add_dependency('task3', 'task2')
    
    # Try to create a cycle
    with pytest.raises(CycleError):
        ts.add_dependency('task1', 'task3')
    
    # Verify scheduler state is unchanged - task1 should still be available
    today = datetime.date.today()
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    assert 'task1' in task_ids, 'task1 should still be available after failed cycle creation'


def test_complete_task_success():
    """Test that complete marks task as done."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    ts = TaskScheduler()
    task = ts.add('task1', 'Test Task')
    
    assert task.done is False, 'Task should start as not done'
    
    ts.complete('task1')
    
    assert task.done is True, 'Task should be marked as done after completion'


def test_complete_unknown_task_error():
    """Test that complete raises UnknownTaskError for unknown id."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    UnknownTaskError = getattr(scheduler, 'UnknownTaskError', None)
    assert UnknownTaskError is not None, 'UnknownTaskError is not implemented yet'
    
    ts = TaskScheduler()
    
    with pytest.raises(UnknownTaskError):
        ts.complete('unknown_task')


def test_complete_blocked_task_error():
    """Test that complete raises BlockedTaskError when dependencies not done."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    BlockedTaskError = getattr(scheduler, 'BlockedTaskError', None)
    assert BlockedTaskError is not None, 'BlockedTaskError is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'First Task')
    ts.add('task2', 'Second Task')
    ts.add_dependency('task2', 'task1')
    
    # Try to complete task2 before task1
    with pytest.raises(BlockedTaskError):
        ts.complete('task2')
    
    # Complete task1 first, then task2 should work
    ts.complete('task1')
    ts.complete('task2')  # Should not raise


def test_next_up_dependency_filtering():
    """Test that next_up returns only tasks whose dependencies are all done."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'Independent Task')
    ts.add('task2', 'Depends on task1')
    ts.add('task3', 'Depends on task2')
    ts.add('task4', 'Another independent')
    
    ts.add_dependency('task2', 'task1')
    ts.add_dependency('task3', 'task2')
    
    today = datetime.date.today()
    
    # Initially, only task1 and task4 should be available
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    assert 'task1' in task_ids, 'task1 should be available'
    assert 'task4' in task_ids, 'task4 should be available'
    assert 'task2' not in task_ids, 'task2 should be blocked'
    assert 'task3' not in task_ids, 'task3 should be blocked'
    
    # Complete task1, now task2 should be available
    ts.complete('task1')
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    assert 'task2' in task_ids, 'task2 should now be available'
    assert 'task4' in task_ids, 'task4 should still be available'
    assert 'task3' not in task_ids, 'task3 should still be blocked'
    assert 'task1' not in task_ids, 'task1 should not appear (completed)'


def test_next_up_ordering():
    """Test next_up ordering: overdue, priority, due date, insertion order."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    Priority = getattr(scheduler, 'Priority', None)
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    ts = TaskScheduler()
    today = datetime.date(2024, 1, 15)
    
    # Add tasks in specific order to test sorting
    ts.add('low_overdue', 'Low Priority Overdue', Priority.LOW, datetime.date(2024, 1, 10))
    ts.add('high_future', 'High Priority Future', Priority.HIGH, datetime.date(2024, 1, 20))
    ts.add('medium_today', 'Medium Priority Today', Priority.MEDIUM, today)
    ts.add('high_overdue', 'High Priority Overdue', Priority.HIGH, datetime.date(2024, 1, 12))
    ts.add('no_due_high', 'No Due High', Priority.HIGH)
    ts.add('no_due_low', 'No Due Low', Priority.LOW)
    ts.add('medium_future', 'Medium Future', Priority.MEDIUM, datetime.date(2024, 1, 18))
    
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    # Expected order:
    # 1. Overdue tasks first (by priority: high_overdue, low_overdue)
    # 2. Then non-overdue by priority, due date, insertion order
    expected_order = [
        'high_overdue',     # Overdue + HIGH priority
        'low_overdue',      # Overdue + LOW priority
        'medium_today',     # Today (not overdue) + MEDIUM priority
        'high_future',      # Future + HIGH priority + earlier due
        'medium_future',    # Future + MEDIUM priority
        'no_due_high',      # No due + HIGH priority + earlier insertion
        'no_due_low'        # No due + LOW priority
    ]
    
    assert task_ids == expected_order, f'Expected order {expected_order}, got {task_ids}'


def test_json_round_trip():
    """Test that to_json and from_json preserve all state."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    Priority = getattr(scheduler, 'Priority', None)
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    # Create original scheduler with complex state
    ts1 = TaskScheduler()
    due_date = datetime.date(2024, 1, 15)
    
    task1 = ts1.add('task1', 'First Task', Priority.HIGH, due_date)
    task2 = ts1.add('task2', 'Second Task', Priority.LOW)
    task3 = ts1.add('task3', 'Third Task', Priority.MEDIUM, datetime.date(2024, 1, 20))
    
    ts1.add_dependency('task2', 'task1')
    ts1.add_dependency('task3', 'task1')
    ts1.complete('task1')
    
    # Serialize and deserialize
    json_str = ts1.to_json()
    assert isinstance(json_str, str), 'to_json should return a string'
    
    # Verify it's valid JSON
    json.loads(json_str)  # Should not raise
    
    ts2 = TaskScheduler.from_json(json_str)
    
    # Compare next_up results
    today = datetime.date(2024, 1, 16)
    next1 = ts1.next_up(today)
    next2 = ts2.next_up(today)
    
    assert len(next1) == len(next2), 'Restored scheduler should have same number of next tasks'
    
    for t1, t2 in zip(next1, next2):
        assert t1.task_id == t2.task_id, 'Task IDs should match'
        assert t1.title == t2.title, 'Task titles should match'
        assert t1.priority == t2.priority, 'Task priorities should match'
        assert t1.due == t2.due, 'Task due dates should match'
        assert t1.done == t2.done, 'Task done status should match'


def test_exception_hierarchy():
    """Test that all scheduler exceptions inherit correctly."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    SchedulerError = getattr(scheduler, 'SchedulerError', None)
    assert SchedulerError is not None, 'SchedulerError is not implemented yet'
    
    DuplicateTaskError = getattr(scheduler, 'DuplicateTaskError', None)
    assert DuplicateTaskError is not None, 'DuplicateTaskError is not implemented yet'
    
    UnknownTaskError = getattr(scheduler, 'UnknownTaskError', None)
    assert UnknownTaskError is not None, 'UnknownTaskError is not implemented yet'
    
    CycleError = getattr(scheduler, 'CycleError', None)
    assert CycleError is not None, 'CycleError is not implemented yet'
    
    BlockedTaskError = getattr(scheduler, 'BlockedTaskError', None)
    assert BlockedTaskError is not None, 'BlockedTaskError is not implemented yet'
    
    # Test inheritance from SchedulerError
    assert issubclass(DuplicateTaskError, SchedulerError), 'DuplicateTaskError should inherit from SchedulerError'
    assert issubclass(UnknownTaskError, SchedulerError), 'UnknownTaskError should inherit from SchedulerError'
    assert issubclass(CycleError, SchedulerError), 'CycleError should inherit from SchedulerError'
    assert issubclass(BlockedTaskError, SchedulerError), 'BlockedTaskError should inherit from SchedulerError'
    
    # Test additional inheritance requirements
    assert issubclass(UnknownTaskError, KeyError), 'UnknownTaskError should also inherit from KeyError'
    assert issubclass(DuplicateTaskError, ValueError), 'DuplicateTaskError should also inherit from ValueError'
    assert issubclass(CycleError, ValueError), 'CycleError should also inherit from ValueError'
    assert issubclass(BlockedTaskError, ValueError), 'BlockedTaskError should also inherit from ValueError'
