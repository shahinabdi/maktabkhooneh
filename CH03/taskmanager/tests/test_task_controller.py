from unittest.mock import patch

import pytest


class TestTaskController:
    @pytest.mark.smoke
    def test_handle_start_task(self, task_controller, monkeypatch):
        user_input = "test task  "
        monkeypatch.setattr("builtins.input", lambda _: user_input)

        task_controller.handle_start_task()
        assert task_controller.model.current_task == "test task"

    @pytest.mark.parametrize(
        "menu_choice, expected_calls",
        [
            ("1", "handle_start_task"),
            ("2", "handle_stop_task"),
            ("3", "handle_view_tasks"),
            ("4", "handle_delete_task"),
            ("5", "handle_exit"),
        ],
    )
    def test_handle_menu_choice(
        self, task_controller, monkeypatch, menu_choice, expected_calls
    ):
        called_method = None

        def mock_handler():
            nonlocal called_method
            called_method = expected_calls
            if menu_choice == "5":
                return True
            return None

        monkeypatch.setattr(task_controller, expected_calls, mock_handler)

        if menu_choice == "5":
            with patch("builtins.input", return_value=menu_choice):
                task_controller.run()
        else:
            with patch("builtins.input", side_effect=[menu_choice, "5"]):
                task_controller.run()
        assert called_method == expected_calls

    def test_handle_invalid_menu_choice(self, task_controller, monkeypatch, capsys):
        """Test stderr in invalid choice"""
        inputs = iter(["invalid", "5"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))
        task_controller.run()
        captured = capsys.readouterr()
        assert "Error: Invalid choice" in captured.out

    @pytest.mark.slow
    def test_handle_view_tasks_complete_flow(
        self, task_controller, monkeypatch, mock_tasks_data
    ):
        task_controller.model.tasks = mock_tasks_data

        inputs = iter(["1", "2", "4"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with patch("builtins.print") as mock_print:
            task_controller.handle_view_tasks()

        calls = mock_print.call_args_list
        assert any("Task: coding" in str(c) for c in calls)
        assert any("Total time: 3600.00 seconds" in str(c) for c in calls)
