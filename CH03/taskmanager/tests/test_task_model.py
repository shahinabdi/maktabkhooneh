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

    def test_start_task_with_running_task(self, task_model):
        """Test starting task when another is running"""
        task_model.start_task("task2")
        with pytest.raises(Exception, match="One task is already running!"):
            task_model.start_task("task2")

    @pytest.mark.smoke
    def test_stop_task_basic_flow(self, task_model, mock_datetime):
        """Test basic task stop functionality"""
        mock_datetime.reset()
        task_model.start_task("test_task")
        result = task_model.stop_task()

        assert result["task_name"] == "test_task"
        assert result["duration"] == 1800
        assert task_model.current_task is None
        assert "test_task" in task_model.tasks
        assert task_model.tasks["test_task"]["total_time"] == 1800
