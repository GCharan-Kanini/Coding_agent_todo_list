import pytest
from io import StringIO

# Existing modules and functions used by regression tests
from src.cli.cli import _handle_add_args, handle_view, main as cli_main
from src.domain.task import create_task
from src.repository import in_memory_repository as repo
from src.cli.interactive_add import run_interactive_add

# The following imports refer to planned/new behaviour (handlers, dispatcher,
# entrypoint and repository mutation helpers). They are intentionally imported at
# module import time so the test collection will fail (RED) until the task
# implements them as described by the plan. This provides the explicit signal
# that the new behaviour is missing. Names chosen follow the project's naming
# conventions described in the task plan.
from src.cli.cli import handle_mark_completed, handle_delete, dispatch_command
from src.cli.main_loop import run_main_loop
from src.cli.entrypoint import main as entrypoint_main
from src.repository.in_memory_repository import update_task_status, remove_task


def setup_function(function):
    # Ensure repository is emptied before each test for determinism
    repo.clear_tasks_for_testing()


def test_ac1_1_add_creates_task(capsys):
    """AC-1.1: non-interactive add should create a Pending task in the repository.

    Given the repository is cleared, when we call the non-interactive add
    handler with a non-empty title, then list_tasks returns a single Task with
    the provided title and status 'Pending'.
    """
    # Sanity: repository starts empty
    assert repo.list_tasks() == []

    # Call the non-interactive add handler with a valid title
    _handle_add_args("Buy milk")

    tasks = repo.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy milk"
    assert tasks[0].status == "Pending"


def test_ac2_1_rejects_empty_title(capsys):
    """AC-2.1: empty/whitespace-only title is rejected by domain and CLI.

    Domain-level create_task should raise ValueError for a whitespace-only
    title. The CLI non-interactive path should print a recoverable error and
    not append a task.
    """
    # Domain-level rejection
    with pytest.raises(ValueError):
        create_task("   ")

    # Non-interactive CLI path prints an error and does not append
    _handle_add_args("   ")
    captured = capsys.readouterr()
    assert "Task title must not be empty" in captured.out
    assert repo.list_tasks() == []


def test_ac3_1_view_shows_numbered_lines(capsys):
    """AC-3.1: view/list prints exactly one numbered line per task.

    Create three tasks with explicit statuses and assert the view output
    contains exactly three lines in the expected '<index>. <title> - <status>'
    format. The CLI's view implementation prints 1-based indices.
    """
    create_task("First task")
    create_task("Second task")
    create_task("Third task", status="Completed")

    assert len(repo.list_tasks()) == 3

    handle_view()
    captured = capsys.readouterr()
    out_lines = [ln for ln in captured.out.splitlines() if ln.strip()]

    assert len(out_lines) == 3
    assert out_lines[0] == "1. First task - Pending"
    assert out_lines[1] == "2. Second task - Pending"
    assert out_lines[2] == "3. Third task - Completed"


def test_ac4_1_mark_completed_updates_status():
    """AC-4.1: mark-completed handler sets the selected task status to 'Completed'.

    This test calls the planned mark-completed handler with index 0 and asserts
    the repository reflects the status change.
    """
    # Prepare repository with one pending task
    create_task("Todo")
    assert repo.list_tasks()[0].status == "Pending"

    # Call the (planned) handler using zero-based index per example
    handle_mark_completed(0)

    assert repo.list_tasks()[0].status == "Completed"


def test_ac5_1_mark_completed_invalid_selection_reprompts():
    """AC-5.1: invalid selection for mark-completed produces a controlled error.

    Calling the mark-completed handler with a non-numeric selection or an
    out-of-range index should raise a controlled ValueError (or similar) and
    must not cause an uncaught exception.
    """
    create_task("One")

    # Non-numeric selection scenario: the handler is expected to validate input
    with pytest.raises(ValueError):
        # The handler is specified to accept an index; passing a string imitates
        # the parsing layer passing an invalid value and the handler raising
        # a controlled error.
        handle_mark_completed("foo")

    # Out-of-range index scenario
    with pytest.raises(ValueError):
        handle_mark_completed(999)

    # The repository must be unchanged after invalid attempts
    tasks_after = repo.list_tasks()
    assert len(tasks_after) == 1
    assert tasks_after[0].title == "One"
    assert tasks_after[0].status == "Pending"


def test_ac6_1_delete_confirms_and_removes():
    """AC-6.1: delete with confirmation removes the task from repository.

    Create two tasks, delete the first by calling the planned delete handler
    and simulating confirmation, then assert repository length decreased and the
    deleted title is not present.
    """
    create_task("Keep me")
    create_task("Delete me")

    initial = repo.list_tasks()
    assert len(initial) == 2

    # Call planned delete handler: assume signature (index, confirm=True)
    handle_delete(1, confirm=True)

    remaining = repo.list_tasks()
    assert len(remaining) == 1
    assert all(t.title != "Delete me" for t in remaining)


def test_ac7_1_main_loop_exit_returns():
    """AC-7.1: main loop returns gracefully upon receiving 'exit' token.

    The planned main loop accepts an iterator of user input tokens; passing an
    iterator that yields 'exit' once should cause the loop to return normally.
    """
    # run_main_loop is a planned entry point accepting an iterator of strings
    run_main_loop(iter(["exit"]))

    # If we reach here without exception, the behaviour is satisfied
    assert True


def test_ac8_1_entrypoint_handles_malformed_args(capsys):
    """AC-8.1: entrypoint reports errors for malformed arguments without crashing.

    Invoking the planned entrypoint with malformed arguments (e.g., a
    non-numeric index for mark-completed) should result in a controlled error
    (SystemExit with non-zero code or printed user-facing message).
    """
    # Call the planned entrypoint main with argv that includes a malformed arg
    with pytest.raises(SystemExit) as excinfo:
        entrypoint_main(["prog", "mark-completed", "not-a-number"])

    # Ensure non-zero exit code indicates error
    assert excinfo.value.code is not None and excinfo.value.code != 0


def test_ac9_1_dispatcher_routes_commands():
    """AC-9.1: dispatcher routes commands to corresponding handlers.

    The planned dispatch_command function should route simple commands and
    return without raising uncaught exceptions.
    """
    # add (non-interactive)
    dispatch_command("add", {"title": "Dispatched add"})
    assert any(t.title == "Dispatched add" for t in repo.list_tasks())

    # view
    dispatch_command("view", {})

    # mark-completed and delete are planned commands; call with valid args
    # For mark-completed we assume zero-based index per examples
    create_task("To complete")
    dispatch_command("mark-completed", {"index": 0})

    # delete: call with confirmation True via dispatch
    create_task("To delete")
    dispatch_command("delete", {"index": 0, "confirm": True})

    # exit: ensure dispatcher can accept exit without raising
    dispatch_command("exit", {})

    assert True


def test_ac10_1_repository_update_and_remove_preserve_order():
    """AC-10.1: repository operations preserve order and correctly update status.

    Append three tasks, update the status of index 1 to 'Completed', remove
    index 0, and assert remaining tasks preserve original append order and the
    status update is reflected.
    """
    # Append three tasks using domain factory which appends into repository
    create_task("first")
    create_task("second")
    create_task("third")

    assert [t.title for t in repo.list_tasks()] == ["first", "second", "third"]

    # Use planned repository mutation helpers
    update_task_status(1, "Completed")
    remove_task(0)

    remaining = repo.list_tasks()
    assert len(remaining) == 2
    # After removing index 0 (first), the remaining should be ['second', 'third']
    assert [t.title for t in remaining] == ["second", "third"]
    # The updated task (originally index 1) should now be at index 0 and Completed
    assert remaining[0].status == "Completed"
