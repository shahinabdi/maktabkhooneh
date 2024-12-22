import pytest


class TestTaskModel:
    @pytest.mark.smoke
    def test_init_empty_file(self, task_model):
        """Test initialization with empty file"""
        assert task_model.tasks == {}
        assert task_model.current_task is None
        assert task_model.start_time is None

    @pytest.mark.parametrize(
        "task_name,expected",
        [
            ("coding", "coding"),
            ("CODING", "coding"),
            ("         coding       ", "coding"),
            ("pYTHON COding   ", "python coding"),
        ],
    )
    def test_start_task_name_normalization(self, task_model, task_name, expected):
        """Test task name normalization"""
        task_model.start_task(task_name)
        assert task_model.current_task == expected
