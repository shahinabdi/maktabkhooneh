import builtins
from datetime import datetime

import pytest
from src.taskmanager.controllers.task_controller import TaskController
from src.taskmanager.models.task_model import TaskModel
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
def mock_datetime(monkeypatch):
    """Mock datetime for consistent timestamp"""

    class MockDateTime:
        _now = datetime(2024, 1, 1, 10, 0)

        @classmethod
        def now(cls):
            current = cls._now
            cls._now = datetime(
                2024,
                1,
                1,
                current.hour + (1 if current.minute >= 30 else 0),
                (current.minute + 30) % 60,
            )
            return current

        @classmethod
        def fromtimestamp(cls, timestamp):
            return datetime.fromtimestamp(timestamp)

        @classmethod
        def reset(cls):
            cls._now = datetime(2024, 1, 1, 10, 0)

    monkeypatch.setattr("src.taskmanager.models.task_model.datetime", MockDateTime)
    MockDateTime.reset()
    return MockDateTime


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


@pytest.fixture
def task_model(tmp_path):
    test_file = tmp_path / "test_task.json"
    return TaskModel(filename=str(test_file))


@pytest.fixture
def task_controller(task_model, task_view):
    """TaskController instance"""
    return TaskController(task_model, task_view)


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test (quick sanity check)"
    )
    config.addinivalue_line("markers", "slow: mark test as slow running")
