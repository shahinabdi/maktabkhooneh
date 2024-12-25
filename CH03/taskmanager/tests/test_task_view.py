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
