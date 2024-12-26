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
