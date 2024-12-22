from datetime import datetime

import pytest
from src.taskmanager.models.task_model import TaskModel


@pytest.fixture
def task_model(tmp_path):
    test_file = tmp_path / "test_task.json"
    return TaskModel(filename=str(test_file))


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
