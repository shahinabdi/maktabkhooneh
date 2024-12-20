import os
import sys

# Current directory
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from controllers.task_controller import TaskController
from models.task_model import TaskModel
from views.task_view import TaskView


def main():
    try:
        model = TaskModel()
        view = TaskView()
        controller = TaskController(model, view)
        controller.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        print("Application terminated due to an error")


if __name__ == "__main__":
    main()
