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
def mock_stdin(monkeypatch):
    """Mock stdin for input"""

    class MockInput:
        def __init__(self):
            self.responses = []

        def __call__(self, prompt):
            if not self.responses:
                return "default"
            return self.responses.pop(0)

        def add_response(self, *responses):
            self.responses.extend(responses)

    mock = MockInput()
    monkeypatch.setattr(builtins, "input", mock)
    return mock


@pytest.fixture
def mock_tasks_data():
    """Sample task data for testing"""
    return {
        "coding": {
            "total_time": 3600,
            "sessions": [
                {
                    "start": "2024-01-01 10:00:00",
                    "end": "2024-01-01 11:00:00",
                    "duration": 3600,
                }
            ],
        }
    }


@pytest.fixture
def task_view():
    """TaskView instance"""
    return TaskView
