import json

import pytest


@pytest.mark.slow
class TestIntegration:
    def test_complete_task_workflow(self, task_controller, mock_stdin, mock_stdout):
        """Test complete task lifecycle"""

        # Setup inputs
        mock_stdin.add_response(
            " test task ",  # TaskName
            "1",  # SelectTask
            "1",  # BasicTaskInfo
            "4",  # BacktoMM
            "1",
        )
        # Run workflow
        task_controller.handle_start_task()
        task_controller.handle_stop_task()
        task_controller.handle_view_tasks()
        task_controller.handle_delete_task()
        # Verify outputs
        output = "\n".join(mock_stdout)
        assert "Task 'test task' started!" in output
        assert "Task 'test task' stopped!" in output
        assert "Task: test task" in output

    @pytest.mark.smoke
    def test_error_handling(
        self, task_controller, mock_stdin, mock_stdout, mock_datetime
    ):
        """Test error handling"""

        mock_datetime.reset()  # Reset mockdatetime

        # Setup inputs
        mock_stdin.add_response("Python", "Java")  # First Task  # Second Task

        task_controller.handle_start_task()

        with pytest.raises(Exception, match="One task is already running!"):
            task_controller.handle_start_task()

        task_controller.handle_stop_task()
        output = "\n".join(mock_stdout)
        assert "Task 'python' stopped!" in output  # Output must be in lowercase
        assert "Duration: 1800.00 seconds" in output

    def test_task_persistence(
        self, task_controller, task_model, mock_stdin, mock_datetime, tmp_path
    ):
        """Test task data persistance"""
        mock_datetime.reset()
        test_file = tmp_path / "test.json"
        task_model.filename = str(test_file)

        # Create and save a task
        mock_stdin.add_response("Test task")
        task_controller.handle_start_task()
        task_controller.handle_stop_task()  # add 30 minutes to the task

        # Verify that the task is saved
        with open(str(test_file), "r") as f:
            saved_task = json.load(f)
            assert "test task" in saved_task
            assert saved_task["test task"]["total_time"] == 1800
