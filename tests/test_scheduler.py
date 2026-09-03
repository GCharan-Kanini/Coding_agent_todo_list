import json
import datetime
import pytest


def get_scheduler_module():
    """Helper to safely import scheduler module."""
    try:
        from todo_app import scheduler
        return scheduler
    except (ImportError, AttributeError):
        return None


def test_priority_enum_members_and_ordering():
    """Test that Priority enum has correct members and ordering."""
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


def test_add_task_returns_correct_task():
    """Test that TaskScheduler.add returns Task with correct attributes."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    Priority = getattr(scheduler, 'Priority', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    ts = TaskScheduler()
    due_date = datetime.date(2024, 1, 15)
    
    # Test with all parameters
    task = ts.add('task1', 'Test Task', Priority.HIGH, due_date)
    
    assert task.task_id == 'task1', 'Task task_id should match input'
    assert task.title == 'Test Task', 'Task title should match input'
    assert task.priority == Priority.HIGH, 'Task priority should match input'
    assert task.due == due_date, 'Task due date should match input'
    assert task.done == False, 'Task done should default to False'
    
    # Test with defaults
    task2 = ts.add('task2', 'Default Task')
    assert task2.priority == Priority.MEDIUM, 'Task priority should default to MEDIUM'
    assert task2.due is None, 'Task due should default to None'
    assert task2.done == False, 'Task done should default to False'


def test_add_duplicate_task_raises_error():
    """Test that adding duplicate task_id raises DuplicateTaskError."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    DuplicateTaskError = getattr(scheduler, 'DuplicateTaskError', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
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
    """Test that add_dependency successfully records dependency."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'First Task')
    ts.add('task2', 'Second Task')
    
    # Should not raise any exception
    ts.add_dependency('task2', 'task1')
    
    # Verify dependency by checking next_up behavior
    today = datetime.date.today()
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    # task2 should not be in next_up since task1 is not done
    assert 'task1' in task_ids, 'task1 should be available'
    assert 'task2' not in task_ids, 'task2 should be blocked by dependency'


def test_add_dependency_unknown_task_error():
    """Test that add_dependency raises UnknownTaskError for unknown task ids."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    UnknownTaskError = getattr(scheduler, 'UnknownTaskError', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert UnknownTaskError is not None, 'UnknownTaskError is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'Existing Task')
    
    # Unknown task_id
    with pytest.raises(UnknownTaskError):
        ts.add_dependency('unknown', 'task1')
    
    # Unknown depends_on
    with pytest.raises(UnknownTaskError):
        ts.add_dependency('task1', 'unknown')


def test_add_dependency_self_cycle_error():
    """Test that add_dependency raises CycleError for self-dependency."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    CycleError = getattr(scheduler, 'CycleError', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert CycleError is not None, 'CycleError is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'Self-dependent Task')
    
    with pytest.raises(CycleError):
        ts.add_dependency('task1', 'task1')


def test_add_dependency_circular_cycle_error():
    """Test that add_dependency raises CycleError for circular dependencies."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    CycleError = getattr(scheduler, 'CycleError', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert CycleError is not None, 'CycleError is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'First Task')
    ts.add('task2', 'Second Task')
    ts.add('task3', 'Third Task')
    
    # Create chain: task1 -> task2 -> task3
    ts.add_dependency('task2', 'task1')
    ts.add_dependency('task3', 'task2')
    
    # Try to create cycle: task3 -> task1 (would create task1 -> task2 -> task3 -> task1)
    with pytest.raises(CycleError):
        ts.add_dependency('task1', 'task3')


def test_complete_task_success():
    """Test that complete marks task as done."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    ts = TaskScheduler()
    task = ts.add('task1', 'Test Task')
    
    assert task.done == False, 'Task should start as not done'
    
    ts.complete('task1')
    
    assert task.done == True, 'Task should be marked as done after completion'


def test_complete_unknown_task_error():
    """Test that complete raises UnknownTaskError for non-existent task."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    UnknownTaskError = getattr(scheduler, 'UnknownTaskError', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert UnknownTaskError is not None, 'UnknownTaskError is not implemented yet'
    
    ts = TaskScheduler()
    
    with pytest.raises(UnknownTaskError):
        ts.complete('nonexistent')


def test_complete_blocked_task_error():
    """Test that complete raises BlockedTaskError when dependencies not done."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    BlockedTaskError = getattr(scheduler, 'BlockedTaskError', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert BlockedTaskError is not None, 'BlockedTaskError is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'Dependency Task')
    ts.add('task2', 'Dependent Task')
    ts.add_dependency('task2', 'task1')
    
    # Try to complete task2 before task1 is done
    with pytest.raises(BlockedTaskError):
        ts.complete('task2')
    
    # Complete task1 first, then task2 should work
    ts.complete('task1')
    ts.complete('task2')  # Should not raise


def test_next_up_dependency_filtering():
    """Test that next_up returns only tasks with completed dependencies."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'Independent Task')
    ts.add('task2', 'Dependent Task')
    ts.add('task3', 'Another Independent')
    ts.add_dependency('task2', 'task1')
    
    today = datetime.date.today()
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    # Only task1 and task3 should be available
    assert 'task1' in task_ids, 'task1 should be available'
    assert 'task3' in task_ids, 'task3 should be available'
    assert 'task2' not in task_ids, 'task2 should be blocked'
    
    # Complete task1, now task2 should be available
    ts.complete('task1')
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    assert 'task2' in task_ids, 'task2 should now be available'
    assert 'task3' in task_ids, 'task3 should still be available'
    assert 'task1' not in task_ids, 'task1 should not appear (completed)'


def test_next_up_overdue_first():
    """Test that next_up returns overdue tasks before non-overdue tasks."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    Priority = getattr(scheduler, 'Priority', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    ts = TaskScheduler()
    today = datetime.date(2024, 1, 15)
    
    # Add overdue task (due yesterday)
    ts.add('overdue', 'Overdue Task', Priority.LOW, datetime.date(2024, 1, 14))
    # Add future task (due tomorrow)
    ts.add('future', 'Future Task', Priority.HIGH, datetime.date(2024, 1, 16))
    
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    # Overdue task should come first despite lower priority
    assert task_ids.index('overdue') < task_ids.index('future'), 'Overdue task should come before future task'


def test_next_up_priority_ordering():
    """Test that next_up orders by priority HIGH before MEDIUM before LOW."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    Priority = getattr(scheduler, 'Priority', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    ts = TaskScheduler()
    today = datetime.date(2024, 1, 15)
    
    # Add tasks with different priorities, all due today
    ts.add('low', 'Low Priority', Priority.LOW, today)
    ts.add('high', 'High Priority', Priority.HIGH, today)
    ts.add('medium', 'Medium Priority', Priority.MEDIUM, today)
    
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    # Should be ordered: high, medium, low
    assert task_ids.index('high') < task_ids.index('medium'), 'HIGH priority should come before MEDIUM'
    assert task_ids.index('medium') < task_ids.index('low'), 'MEDIUM priority should come before LOW'


def test_next_up_due_date_ordering():
    """Test that next_up orders by earlier due date within same priority."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    Priority = getattr(scheduler, 'Priority', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    ts = TaskScheduler()
    today = datetime.date(2024, 1, 15)
    
    # Add tasks with same priority but different due dates
    ts.add('later', 'Later Task', Priority.HIGH, datetime.date(2024, 1, 20))
    ts.add('earlier', 'Earlier Task', Priority.HIGH, datetime.date(2024, 1, 18))
    
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    # Earlier due date should come first
    assert task_ids.index('earlier') < task_ids.index('later'), 'Earlier due date should come before later due date'


def test_next_up_no_due_date_ordering():
    """Test that next_up places tasks with no due date after tasks with due dates."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    Priority = getattr(scheduler, 'Priority', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    ts = TaskScheduler()
    today = datetime.date(2024, 1, 15)
    
    # Add tasks with same priority, one with due date, one without
    ts.add('no_due', 'No Due Date', Priority.HIGH, None)
    ts.add('with_due', 'With Due Date', Priority.HIGH, datetime.date(2024, 1, 20))
    
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    # Task with due date should come before task without due date
    assert task_ids.index('with_due') < task_ids.index('no_due'), 'Task with due date should come before task without due date'


def test_next_up_insertion_order():
    """Test that next_up uses insertion order as final tiebreaker."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    Priority = getattr(scheduler, 'Priority', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    ts = TaskScheduler()
    today = datetime.date(2024, 1, 15)
    
    # Add tasks with identical priority and due date
    ts.add('first', 'First Task', Priority.HIGH, None)
    ts.add('second', 'Second Task', Priority.HIGH, None)
    ts.add('third', 'Third Task', Priority.HIGH, None)
    
    next_tasks = ts.next_up(today)
    task_ids = [task.task_id for task in next_tasks]
    
    # Should maintain insertion order
    assert task_ids.index('first') < task_ids.index('second'), 'First inserted should come before second'
    assert task_ids.index('second') < task_ids.index('third'), 'Second inserted should come before third'


def test_to_json_returns_valid_json():
    """Test that to_json returns a valid JSON string."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    Priority = getattr(scheduler, 'Priority', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    ts = TaskScheduler()
    ts.add('task1', 'Test Task', Priority.HIGH, datetime.date(2024, 1, 15))
    
    json_str = ts.to_json()
    
    # Should be valid JSON
    parsed = json.loads(json_str)
    assert isinstance(parsed, dict), 'JSON should parse to a dictionary'


def test_from_json_reconstructs_scheduler():
    """Test that from_json rebuilds scheduler with identical tasks and dependencies."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    Priority = getattr(scheduler, 'Priority', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    # Create original scheduler
    ts1 = TaskScheduler()
    ts1.add('task1', 'First Task', Priority.HIGH, datetime.date(2024, 1, 15))
    ts1.add('task2', 'Second Task', Priority.MEDIUM, None)
    ts1.add_dependency('task2', 'task1')
    ts1.complete('task1')
    
    # Serialize and deserialize
    json_str = ts1.to_json()
    ts2 = TaskScheduler.from_json(json_str)
    
    # Check tasks are identical
    today = datetime.date(2024, 1, 15)
    tasks1 = ts1.next_up(today)
    tasks2 = ts2.next_up(today)
    
    assert len(tasks1) == len(tasks2), 'Reconstructed scheduler should have same number of available tasks'
    
    for t1, t2 in zip(tasks1, tasks2):
        assert t1.task_id == t2.task_id, 'Task IDs should match'
        assert t1.title == t2.title, 'Task titles should match'
        assert t1.priority == t2.priority, 'Task priorities should match'
        assert t1.due == t2.due, 'Task due dates should match'
        assert t1.done == t2.done, 'Task done status should match'


def test_json_roundtrip_preserves_next_up():
    """Test that next_up gives identical results after JSON round-trip."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    TaskScheduler = getattr(scheduler, 'TaskScheduler', None)
    Priority = getattr(scheduler, 'Priority', None)
    assert TaskScheduler is not None, 'TaskScheduler class is not implemented yet'
    assert Priority is not None, 'Priority enum is not implemented yet'
    
    # Create complex scheduler
    ts1 = TaskScheduler()
    today = datetime.date(2024, 1, 15)
    
    ts1.add('overdue', 'Overdue Task', Priority.LOW, datetime.date(2024, 1, 10))
    ts1.add('high_today', 'High Priority Today', Priority.HIGH, today)
    ts1.add('medium_future', 'Medium Future', Priority.MEDIUM, datetime.date(2024, 1, 20))
    ts1.add('no_due', 'No Due Date', Priority.HIGH, None)
    ts1.add('blocked', 'Blocked Task', Priority.HIGH, today)
    ts1.add_dependency('blocked', 'high_today')
    
    # Get original next_up result
    original_next = ts1.next_up(today)
    original_ids = [task.task_id for task in original_next]
    
    # Round-trip through JSON
    json_str = ts1.to_json()
    ts2 = TaskScheduler.from_json(json_str)
    
    # Get reconstructed next_up result
    reconstructed_next = ts2.next_up(today)
    reconstructed_ids = [task.task_id for task in reconstructed_next]
    
    # Should be identical
    assert original_ids == reconstructed_ids, 'next_up results should be identical after JSON round-trip'


def test_exception_hierarchy_scheduler_error():
    """Test that all scheduler exceptions derive from SchedulerError."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    SchedulerError = getattr(scheduler, 'SchedulerError', None)
    DuplicateTaskError = getattr(scheduler, 'DuplicateTaskError', None)
    UnknownTaskError = getattr(scheduler, 'UnknownTaskError', None)
    CycleError = getattr(scheduler, 'CycleError', None)
    BlockedTaskError = getattr(scheduler, 'BlockedTaskError', None)
    
    assert SchedulerError is not None, 'SchedulerError is not implemented yet'
    assert DuplicateTaskError is not None, 'DuplicateTaskError is not implemented yet'
    assert UnknownTaskError is not None, 'UnknownTaskError is not implemented yet'
    assert CycleError is not None, 'CycleError is not implemented yet'
    assert BlockedTaskError is not None, 'BlockedTaskError is not implemented yet'
    
    # Check inheritance
    assert issubclass(DuplicateTaskError, SchedulerError), 'DuplicateTaskError should inherit from SchedulerError'
    assert issubclass(UnknownTaskError, SchedulerError), 'UnknownTaskError should inherit from SchedulerError'
    assert issubclass(CycleError, SchedulerError), 'CycleError should inherit from SchedulerError'
    assert issubclass(BlockedTaskError, SchedulerError), 'BlockedTaskError should inherit from SchedulerError'


def test_unknown_task_error_is_key_error():
    """Test that UnknownTaskError inherits from both SchedulerError and KeyError."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    SchedulerError = getattr(scheduler, 'SchedulerError', None)
    UnknownTaskError = getattr(scheduler, 'UnknownTaskError', None)
    
    assert SchedulerError is not None, 'SchedulerError is not implemented yet'
    assert UnknownTaskError is not None, 'UnknownTaskError is not implemented yet'
    
    # Check multiple inheritance
    assert issubclass(UnknownTaskError, SchedulerError), 'UnknownTaskError should inherit from SchedulerError'
    assert issubclass(UnknownTaskError, KeyError), 'UnknownTaskError should inherit from KeyError'


def test_other_errors_are_value_errors():
    """Test that DuplicateTaskError, CycleError, BlockedTaskError inherit from ValueError."""
    scheduler = get_scheduler_module()
    assert scheduler is not None, 'todo_app.scheduler module is not implemented yet'
    
    DuplicateTaskError = getattr(scheduler, 'DuplicateTaskError', None)
    CycleError = getattr(scheduler, 'CycleError', None)
    BlockedTaskError = getattr(scheduler, 'BlockedTaskError', None)
    
    assert DuplicateTaskError is not None, 'DuplicateTaskError is not implemented yet'
    assert CycleError is not None, 'CycleError is not implemented yet'
    assert BlockedTaskError is not None, 'BlockedTaskError is not implemented yet'
    
    # Check ValueError inheritance
    assert issubclass(DuplicateTaskError, ValueError), 'DuplicateTaskError should inherit from ValueError'
    assert issubclass(CycleError, ValueError), 'CycleError should inherit from ValueError'
    assert issubclass(BlockedTaskError, ValueError), 'BlockedTaskError should inherit from ValueError'
