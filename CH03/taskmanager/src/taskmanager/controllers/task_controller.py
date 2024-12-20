from models.task_model import TaskModel
from views.task_view import TaskView


class TaskController:
    def __init__(self, model: TaskModel, view: TaskView):
        self.model = model
        self.view = view
