import pytest


class TestTaskView:
    @pytest.mark.smoke
    def test_show_menu(self, task_view, mock_stdout):
        """Test dispaly menu"""
        task_view.show_menu()
        menu_text = "\n".join(mock_stdout)
        assert "=== Task Tracker Menu ===" in menu_text
        assert "2. Stop task" in menu_text
        assert "5. Exit" in menu_text

    def test_get_input(self, task_view, mock_stdin):
        """Test input handling"""
        mock_stdin.add_response("       test input      ")
        result = task_view.get_input("Enter test: ")
        assert result == "test input"

    def test_show_message(self, task_view, mock_stdout):
        """Test message display"""
        message = "Test message"
        task_view.show_message(message)
        assert message in mock_stdout

    def test_show_task_list(self, task_view, mock_stdout):
        """Test task list display"""
        tasks = ["task1", "task2"]
        task_view.show_task_list(tasks)
        output = "\n".join(mock_stdout)
        assert "Available Tasks:" in output
        for i, task in enumerate(tasks, 1):
            assert f"{i}. {task}" in output

    @pytest.mark.parametrize(
        "view_type, show_sessions", [("1", False), ("2", True), ("3", True)]
    )
    def test_show_task_details(
        self, task_view, mock_stdout, mock_tasks_data, view_type, show_sessions
    ):
        """Test task details display"""
        task_view.show_task_details("coding", mock_tasks_data["coding"], view_type)
        output = "\n".join(mock_stdout)
        assert "Task: coding" in output
        assert "Total time: 3600.00 seconds" in output
        if show_sessions:
            assert "Start: 2024-01-01" in output
            assert "Duration: 3600.00 seconds" in output
