import pytest


class TestTaskController:
    @pytest.mark.smoke
    def test_handle_start_task(self, task_controller, monkeypatch):
        user_input = "test task  "
        monkeypatch.setattr("builtins.input", lambda _: user_input)

        task_controller.handle_start_task()
        assert task_controller.model.current_task == "test task"
