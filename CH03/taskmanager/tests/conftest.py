import pytest
from src.taskmanager.models.task_model import TaskModel


@pytest.fixture
def task_model(tmp_path):
    test_file = tmp_path / "test_task.json"
    return TaskModel(filename=str(test_file))
