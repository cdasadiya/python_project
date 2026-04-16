import importlib

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import to_do_checklist_python_list as todo


def reset_state():
    todo.checklist[:] = [
        "Wake up early",
        "Workout",
        "Read 20 pages",
        "Complete Python project",
        "Attend meetings",
        "Plan next day",
    ]
    todo.completed_tasks[:] = []
    todo.incomplete_tasks[:] = []


def setup_function():
    # ensure global mutable state is reset before each test
    importlib.reload(todo)
    reset_state()


def test_display_tasks_shows_no_tasks_for_empty_list(capsys):
    todo.display_tasks([], "Checklist")
    out = capsys.readouterr().out
    assert "Checklist" in out
    assert "No tasks" in out


def test_add_task_adds_unique_task(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Buy groceries")
    todo.add_task()
    assert "Buy groceries" in todo.checklist


def test_add_task_rejects_duplicate_case_insensitive(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "workout")
    original = list(todo.checklist)
    todo.add_task()

    out = capsys.readouterr().out
    assert todo.checklist == original
    assert "Invalid or duplicate task." in out


def test_mark_tasks_splits_completed_and_incomplete(monkeypatch):
    todo.checklist[:] = ["Task A", "Task B"]
    answers = iter(["y", "n"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    todo.mark_tasks()

    assert todo.completed_tasks == ["Task A"]
    assert todo.incomplete_tasks == ["Task B"]
    assert todo.checklist == []
