from importlib import reload

import socket
import urllib.request
from typing import List, Tuple

from src.repository import in_memory_repository as repo
from src.domain import task as domain_task

# The new view handler is expected to exist as planned. Importing it at
# collection time is intentional (greenfield rule): if it's absent the test
# collection will fail which is the RED signal the plan describes.
from src.cli.cli import handle_view


def _reset_repo():
    try:
        repo.clear_tasks_for_testing()
    except Exception:
        reload(repo)


def _titles_and_statuses(tasks) -> List[Tuple[str, str]]:
    return [(t.title, t.status) for t in tasks]


def test_ac1_1_prints_numbered_tasks(capsys):
    """AC-1.1: Given three tasks appended in order, view prints exactly numbered lines

    Given the in-memory repository is cleared and three tasks are appended in order
    When the CLI view handler is invoked in-process
    Then captured stdout contains exactly three numbered lines in order:
      '1. A - Pending', '2. B - Completed', '3. C - Pending'
    """
    _reset_repo()

    # Create tasks in the required order and statuses using the domain helper
    domain_task.create_task('A', status='Pending')
    domain_task.create_task('B', status='Completed')
    domain_task.create_task('C', status='Pending')

    # Invoke the view handler directly
    handle_view()

    out = capsys.readouterr()
    lines = [ln.rstrip('\n') for ln in out.out.splitlines() if ln.strip() != '']

    expected = ['1. A - Pending', '2. B - Completed', '3. C - Pending']
    assert lines == expected


def test_ac2_1_preserves_order_and_status(capsys):
    """AC-2.1: Appended tasks are shown in append order and show exact status text

    Given two tasks appended in order 'First' (Pending), 'Second' (Pending)
    When the view handler is invoked
    Then output lines show tasks in append order and display 'Pending' exactly as stored.
    """
    _reset_repo()

    domain_task.create_task('First')  # defaults to Pending
    domain_task.create_task('Second')

    handle_view()

    out = capsys.readouterr()
    lines = [ln.rstrip('\n') for ln in out.out.splitlines() if ln.strip() != '']

    expected = ['1. First - Pending', '2. Second - Pending']
    assert lines == expected


def test_ac3_1_empty_prints_no_tasks_message(capsys):
    """AC-3.1: Empty repository prints a clear no-tasks message and does not raise

    Given the repository is cleared so no tasks exist
    When the view handler is invoked
    Then captured stdout contains the exact no-tasks message 'No tasks found.' and no exception is raised.
    """
    _reset_repo()

    # Expect a clear message when no tasks exist. The planned behavior example
    # used 'No tasks found.' as the exact text; assert that literal here.
    handle_view()

    out = capsys.readouterr()
    # Allow surrounding whitespace/newlines but require the exact phrase present
    assert 'No tasks found.' in out.out


def test_ac4_1_uses_only_in_memory_repository(capsys, monkeypatch):
    """AC-4.1: View must not perform file or network I/O; spies must not be called

    Given monkeypatch replaces builtins.open and common network entrypoints with spies
    When the CLI view handler is invoked
    Then none of those spies are called and only repository.list_tasks() provides data
    """
    _reset_repo()

    # Populate some tasks so the view will exercise the normal output path
    domain_task.create_task('LocalOnly', status='Pending')

    called = {'open': 0, 'socket': 0, 'urlopen': 0}

    def spy_open(*args, **kwargs):
        called['open'] += 1
        raise AssertionError('builtins.open was called during view')

    def spy_socket(*args, **kwargs):
        called['socket'] += 1
        raise AssertionError('socket.socket was called during view')

    def spy_urlopen(*args, **kwargs):
        called['urlopen'] += 1
        raise AssertionError('urllib.request.urlopen was called during view')

    monkeypatch.setattr('builtins.open', spy_open)
    monkeypatch.setattr(socket, 'socket', spy_socket)
    monkeypatch.setattr(urllib.request, 'urlopen', spy_urlopen)

    # If any of the spies are invoked, they will raise an AssertionError and fail
    # the test. Otherwise this call should complete normally and produce output.
    handle_view()

    out = capsys.readouterr()
    lines = [ln.rstrip('\n') for ln in out.out.splitlines() if ln.strip() != '']
    assert lines == ['1. LocalOnly - Pending']

    # Explicitly assert that our counters remain zero (spies didn't run)
    assert called['open'] == 0
    assert called['socket'] == 0
    assert called['urlopen'] == 0


def test_ac5_1_does_not_modify_repository():
    """AC-5.1: View returns control and leaves repository unchanged

    Given repository contains two tasks
    When invoke the view handler
    Then after handler returns, repository.list_tasks() returns the same tasks in the same order
    """
    _reset_repo()

    domain_task.create_task('Keep1', status='Pending')
    domain_task.create_task('Keep2', status='Completed')

    before = _titles_and_statuses(repo.list_tasks())

    # Call view; should not raise or mutate repository
    handle_view()

    after = _titles_and_statuses(repo.list_tasks())

    assert before == after
