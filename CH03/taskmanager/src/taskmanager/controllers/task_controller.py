from models.task_model import TaskModel
from views.task_view import TaskView


class TaskController:
    def __init__(self, model: TaskModel, view: TaskView):
        self.model = model
        self.view = view

    def run(self) -> None:
        while True:
            try:
                self.view.show_menu()
                choice = self.view.get_input("Choose option: ")
                if choice == "1":
                    self.handle_start_task()
                elif choice == "2":
                    self.handle_stop_task()
                elif choice == "3":
                    self.handle_view_tasks()
                elif choice == "4":
                    self.handle_delete_task()
                elif choice == "5":
                    self.handle_exit()
                    break
                else:
                    self.view.show_error("Invalid choice")
            except Exception as e:
                self.view.show_error(str(e))

    def handle_start_task(self) -> None:
        task_name = self.view.get_input("Enter task name: ")
        self.model.start_task(task_name)
        self.view.show_message(f"Task '{task_name}' started!")

    def handle_stop_task(self) -> None:
        pass

    def handle_view_tasks(self) -> None:
        pass

    def handle_delete_task(self) -> None:
        pass

    def handle_exit(self) -> None:
        pass
