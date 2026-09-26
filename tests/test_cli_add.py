from importlib import reload

import pytest

from src.repository import in_memory_repository as repo
from src.domain import task as domain_task

# The CLI modules below are part of the planned new behaviour. Import them
# directly so collection fails (RED) if they are absent as the plan expects.
from src.cli.cli import main
from src.cli.interactive_add import run_interactive_add


def _reset_repo():
    # Prefer the repository's own clearing helper if present, otherwise reload
    # the module to reset module-level state between tests.
    try:
        repo.clear_tasks_for_testing()
    except Exception:
        reload(repo)


def test_ac3_1_non_interactive_creates_task(capsys):
    """AC-3.1: non-interactive add with a valid title prints success and creates the task

    Given an empty repository
    When main(['prog', 'add', 'My Task']) is invoked
    Then stdout contains a success indicator (title present) and list_tasks() has
    a Task with title 'My Task' and status 'Pending'
    """
    _reset_repo()

    main(['prog', 'add', 'My Task'])

    out = capsys.readouterr()

    # The implementation is expected to print a success message that includes
    # the provided title. Assert the title is present in output, and that the
    # repository contains the new pending task.
    assert 'My Task' in (out.out + out.err)

    tasks = repo.list_tasks()
    assert len(tasks) == 1
    t = tasks[0]
    assert t.title == 'My Task'
    assert t.status == 'Pending'


def test_ac3_2_non_interactive_empty_title_shows_validation_and_no_task(capsys):
    """AC-3.2: non-interactive add with empty/whitespace title shows validation and does not create task

    Given an empty repository
    When main(['prog', 'add', ' ']) is invoked
    Then the output contains a validation error and the repository remains empty
    """
    _reset_repo()

    # Call with a whitespace-only title which domain.create_task rejects.
    main(['prog', 'add', ' '])

    out = capsys.readouterr()

    # The domain's validation message includes the phrase 'must not be empty'.
    assert 'must not be empty' in (out.out + out.err)

    tasks = repo.list_tasks()
    assert len(tasks) == 0


def test_ac4_1_interactive_creates_task(monkeypatch):
    """AC-4.1: interactive add where prompt returns a valid title creates the task

    Given prompt_toolkit.prompt returns 'Interactive Title' and an empty repository
    When run_interactive_add(repo) is invoked
    Then list_tasks() contains the new task titled 'Interactive Title' with status 'Pending'
    """
    _reset_repo()

    def fake_prompt(*args, **kwargs):
        return 'Interactive Title'

    monkeypatch.setattr('prompt_toolkit.prompt', fake_prompt)

    # The interactive function accepts the repository module as planned.
    run_interactive_add(repo)

    tasks = repo.list_tasks()
    assert len(tasks) == 1
    t = tasks[0]
    assert t.title == 'Interactive Title'
    assert t.status == 'Pending'


def test_ac5_1_interactive_reprompts_on_empty_then_creates(capsys, monkeypatch):
    """AC-5.1: interactive add reprompts after empty input and then creates task

    Given prompt_toolkit.prompt returns '' then 'Good Title'
    When run_interactive_add(repo) runs
    Then the first prompt produced a validation message and no task was created; after the second prompt a task is created
    """
    _reset_repo()

    replies = ['', 'Good Title']

    def seq_prompt(*args, **kwargs):
        try:
            return replies.pop(0)
        except IndexError:
            # If the code prompts more than expected, raise to fail the test.
            raise RuntimeError('prompt called too many times')

    monkeypatch.setattr('prompt_toolkit.prompt', seq_prompt)

    run_interactive_add(repo)

    out = capsys.readouterr()

    # The validation message should mention non-empty requirement coming from
    # domain validation; assert substring present.
    assert 'must not be empty' in (out.out + out.err)

    tasks = repo.list_tasks()
    assert len(tasks) == 1
    t = tasks[0]
    assert t.title == 'Good Title'
    assert t.status == 'Pending'


def test_ac6_1_non_interactive_calls_domain_create_task(monkeypatch):
    """AC-6.1: non-interactive add calls domain.create_task and creates the pending task

    Given an empty repository
    When main(['prog', 'add', 'Title']) is invoked
    Then domain.create_task is called and the repository contains the new pending task
    """
    _reset_repo()

    called = {'count': 0}
    original_create = domain_task.create_task

    def spy_create(title, status=None):
        called['count'] += 1
        return original_create(title, status)

    monkeypatch.setattr(domain_task, 'create_task', spy_create)

    main(['prog', 'add', 'Title'])

    assert called['count'] == 1

    tasks = repo.list_tasks()
    assert len(tasks) == 1
    t = tasks[0]
    assert t.title == 'Title'
    assert t.status == 'Pending'


def test_ac7_1_interactive_cancel_does_not_create_task_and_prints_message(capsys, monkeypatch):
    """AC-7.1: interactive add where user cancels (KeyboardInterrupt) results in no task and a cancel message

    Given prompt_toolkit.prompt raises KeyboardInterrupt
    When run_interactive_add(repo) runs
    Then no task is created and output contains an indication of cancellation
    """
    _reset_repo()

    def raise_cancel(*args, **kwargs):
        raise KeyboardInterrupt()

    monkeypatch.setattr('prompt_toolkit.prompt', raise_cancel)

    # The interactive flow is expected to handle KeyboardInterrupt and return
    # without creating a task.
    run_interactive_add(repo)

    out = capsys.readouterr()

    tasks = repo.list_tasks()
    assert len(tasks) == 0

    # Assert some cancellation feedback was printed; check for the substring
    # 'cancel' case-insensitively to allow spelling variations (cancel/cancelled).
    assert 'cancel' in (out.out + out.err).lower()


def test_ac8_1_non_interactive_calls__append_task_once(monkeypatch):
    """AC-8.1: non-interactive add with valid title calls the repository _append_task exactly once

    Given an empty repository and a spy on _append_task
    When main(['prog', 'add', 'Spy Title']) runs
    Then the spy observed exactly one call and the repository increased by one
    """
    _reset_repo()

    original_append = repo._append_task
    calls = {'count': 0}

    def spy_append(task):
        calls['count'] += 1
        return original_append(task)

    monkeypatch.setattr(repo, '_append_task', spy_append)

    main(['prog', 'add', 'Spy Title'])

    assert calls['count'] == 1

    tasks = repo.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == 'Spy Title'
    assert tasks[0].status == 'Pending'


def test_ac8_2_interactive_cancel_does_not_call__append_task(monkeypatch):
    """AC-8.2: interactive cancel does not call repository._append_task

    Given a spy on _append_task and prompt_toolkit.prompt raising KeyboardInterrupt
    When run_interactive_add(repo) runs
    Then the spy was not called and list_tasks() remains empty
    """
    _reset_repo()

    original_append = repo._append_task
    calls = {'count': 0}

    def spy_append(task):
        calls['count'] += 1
        return original_append(task)

    monkeypatch.setattr(repo, '_append_task', spy_append)

    def raise_cancel(*args, **kwargs):
        raise KeyboardInterrupt()

    monkeypatch.setattr('prompt_toolkit.prompt', raise_cancel)

    run_interactive_add(repo)

    assert calls['count'] == 0

    tasks = repo.list_tasks()
    assert len(tasks) == 0
