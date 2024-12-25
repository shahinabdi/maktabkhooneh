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
