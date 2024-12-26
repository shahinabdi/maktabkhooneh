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

    def test_delete_task(self, task_model, mock_tasks_data):
        """Test task deletion"""
        task_model.tasks = mock_tasks_data.copy()
        task_model.delete_task("coding")
        assert "coding" not in task_model.tasks

    def test_delete_task_not_exist(self, task_model):
        """Test delete task not exist"""
        with pytest.raises(Exception, match="Task not found"):
            task_model.delete_task("python")

    def test_get_all_tasks_sorted(self, task_model):
        """Test tasks are return sorted"""
        task_model.tasks = {"zebra": {}, "alpha": {}, "gamma": {}, "beta": {}}
        assert task_model.get_all_tasks() == ["alpha", "beta", "gamma", "zebra"]

    def test_get_task_details(self, task_model, mock_tasks_data):
        """Test task details"""
        task_model.tasks = mock_tasks_data.copy()
        details = task_model.get_task_details("coding")
        assert details["total_time"] == 3600
        assert len(details["sessions"]) == 1
        assert details["sessions"][0]["duration"] == 3600
