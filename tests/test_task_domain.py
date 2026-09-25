import importlib
import pytest

from src.domain import task as task_module
from src.repository import in_memory_repository as repo_module


def _reload_modules():
    importlib.reload(task_module)
    importlib.reload(repo_module)


def _get_api():
    # access functions/objects from the reloaded modules inside tests
    create_task = getattr(task_module, "create_task")
    Task = getattr(task_module, "Task")
    list_tasks = getattr(repo_module, "list_tasks")
    return create_task, Task, list_tasks


def test_create_task_raises_on_empty_whitespace_title_and_invalid_status():
    """AC-1 / AC-6 / AC-7

    Attempting to create tasks with empty or whitespace-only titles or invalid status
    must raise a validation error and must not change the in-memory task list.
    """
    _reload_modules()
    create_task, Task, list_tasks = _get_api()

    before = list(list_tasks())
    before_len = len(before)

    # empty title
    with pytest.raises(ValueError):
        create_task("")

    # whitespace-only title
    with pytest.raises(ValueError):
        create_task("   \t\n  ")

    # invalid status value (not 'Pending' or 'Completed')
    with pytest.raises(ValueError):
        create_task("Valid Title", status="NotAValidStatus")

    # ensure repository unchanged after failed attempts
    after = list(list_tasks())
    assert len(after) == before_len
    assert after == before


def test_create_task_appends_pending_by_default_and_increases_repository_length():
    """AC-2 / AC-3 / AC-8

    Creating a task non-interactively with a non-empty title should default status
    to 'Pending', append the task to the in-memory list and make it visible to
    subsequent list_tasks() calls in the same process.
    """
    _reload_modules()
    create_task, Task, list_tasks = _get_api()

    before = list(list_tasks())
    before_len = len(before)

    created = create_task("My non-interactive test task")

    # The created object must expose a status and it must default to 'Pending'
    assert hasattr(created, "status")
    assert created.status == "Pending"

    # repository length increased by exactly 1
    after = list(list_tasks())
    assert len(after) == before_len + 1

    # the newly created task must be visible in the repository
    # Prefer identity equality; if implementation returns the same object the test will pass here.
    assert any(t is created for t in after), (
        "Created task object is not the same identity as any repository element; "
        "fallback: assert by matching title and status"
    )

    # fallback assertion by attribute values to ensure the task data exists in repo
    assert any(getattr(t, "title", None) == getattr(created, "title", None) and getattr(t, "status", None) == getattr(created, "status", None) for t in after)


def test_create_task_accepts_completed_status_and_preserves_title_whitespace_and_special_chars():
    """AC-10 / AC-7 / AC-8

    Creating a task with an explicit allowed status ('Completed') must be accepted.
    Titles containing leading/trailing whitespace and special characters must be preserved exactly.
    """
    _reload_modules()
    create_task, Task, list_tasks = _get_api()

    title = "  \tSpecial Title! \n with unicode: Ω ≈  "

    created = create_task(title, status="Completed")

    # exact preservation of title string
    assert getattr(created, "title") == title

    # status honored
    assert getattr(created, "status") == "Completed"

    # ensure visibility in the in-memory repository
    after = list(list_tasks())
    assert any(getattr(t, "title", None) == title and getattr(t, "status", None) == "Completed" for t in after)

    # prefer identity equality to ensure the returned object is the stored object
    assert any(t is created for t in after)


def test_list_tasks_returns_a_copy_and_does_not_create_files(tmp_path):
    """AC-9

    list_tasks() must return a list view suitable for callers; mutating the returned
    list should not change the repository's internal list (i.e. it should behave as a copy).
    Also assert that listing tasks does not cause writes to an unrelated filesystem location (tmp_path)
    during the call.
    """
    _reload_modules()
    create_task, Task, list_tasks = _get_api()

    # Ensure there's at least one task to observe
    create_task("task for list copy test")

    # snapshot contents of the provided tmp_path before calling list_tasks
    before_entries = list(tmp_path.iterdir())

    returned = list_tasks()
    assert isinstance(returned, list)

    returned_len = len(returned)

    # Mutate the returned list and assert repository view is unchanged
    returned.append(object())
    assert len(list_tasks()) == returned_len

    # Ensure nothing was written into tmp_path by these operations
    after_entries = list(tmp_path.iterdir())
    assert before_entries == after_entries
