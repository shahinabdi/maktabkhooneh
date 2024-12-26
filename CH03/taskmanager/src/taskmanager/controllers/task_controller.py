from src.taskmanager.models.task_model import TaskModel
from src.taskmanager.views.task_view import TaskView


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
        result = self.model.stop_task()
        self.view.show_message(
            f"Task '{result['task_name']}' stopped! Duration: {result['duration']:.2f} seconds"
        )

    def handle_view_tasks(self) -> None:
        tasks = self.model.get_all_tasks()

        if not tasks:
            self.view.show_message("No tasks recorded!")
            return

        self.view.show_task_list(tasks)
        task_num = self.view.get_input("Enter task number to view (0 to cancel): ")
        if task_num == "0":
            return

        try:
            task_index = int(task_num) - 1
            if 0 <= task_index < len(tasks):
                task_name = tasks[task_index]

                while True:
                    self.view.show_task_options()
                    view_choice = self.view.get_input("Choose view option: ")

                    if view_choice == "4":
                        break

                    if view_choice in ["1", "2", "3"]:
                        task_data = self.model.get_task_details(task_name)
                        self.view.show_task_details(task_name, task_data, view_choice)
                    else:
                        self.view.show_error("Invalid view option")
            else:
                self.view.show_error("Invalid task number")
        except ValueError:
            self.view.show_error("Please enter a valid number")

    def handle_delete_task(self) -> None:
        tasks = self.model.get_all_tasks()
        if not tasks:
            self.view.show_message("No tasks to delete!")
            return

        self.view.show_task_list(tasks)
        task_num = self.view.get_input("Enter task number to delete (0 to cancel): ")

        if task_num == "0":
            return

        try:
            task_index = int(task_num) - 1
            if 0 <= task_index < len(tasks):
                task_name = tasks[task_index]
                self.model.delete_task(task_name)
                self.view.show_message(f"Task '{task_name}' deleted!")
            else:
                self.view.show_error("Invalid task number")
        except ValueError:
            self.view.show_error("Please enter a valid number")

    def handle_exit(self) -> bool:
        if self.model.get_current_task() is not None:
            self.view.show_error("Please stop the current task first!")
            self.view.show_message(
                f"Task: {self.model.get_current_task()} Status: Running"
            )
            return False
        self.view.show_message("Goodbye!")
        return True
