from models.task_model import TaskModel
from views.task_view import TaskView


class TaskController:
    def __init__(self, model: TaskModel, view: TaskView):
        self.model = model
        self.view = view

    def run(self) -> None:
        pass

    def handle_start_task(self) -> None:
        pass

    def handle_stop_task(self) -> None:
        pass

    def handle_view_tasks(self) -> None:
        pass

    def handle_delete_task(self) -> None:
        pass

    def handle_exit(self) -> None:
        pass
