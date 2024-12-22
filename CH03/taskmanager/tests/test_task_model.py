import pytest


class TestTaskModel:
    @pytest.mark.smoke
    def test_init_empty_file(self, task_model):
        """Test initialization with empty file"""
        assert task_model.tasks == {}
        assert task_model.current_task is None
        assert task_model.start_time is None
