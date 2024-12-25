import builtins

import pytest
from src.taskmanager.views.task_view import TaskView


@pytest.fixture
def mock_stdout(monkeypatch):
    """Mock stdout to prevent print in terminal"""
    outputs = []

    def mock_print(*args, **kwargs):
        outputs.append(" ".join(str(arg) for arg in args))

    monkeypatch.setattr(builtins, "print", mock_print)
    return outputs


@pytest.fixture
def task_view():
    """TaskView instance"""
    return TaskView
