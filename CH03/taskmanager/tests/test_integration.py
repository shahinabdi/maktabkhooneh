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
