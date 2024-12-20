from typing import Dict, List


class TaskView:
    @staticmethod
    def show_menu() -> None:
        print("\n === Task Tracker Menu ===")
        print("1. Start task")
        print("2. Stop task")
        print("3. View task")
        print("4. Delete task")
        print("5. Exit")

    @staticmethod
    def get_input(prompt: str) -> str:
        return input(prompt).strip()

    @staticmethod
    def show_message(message: str) -> None:
        print(message)

    @staticmethod
    def show_error(error: str) -> None:
        print(f"Error: {error}")

    @staticmethod
    def show_task_list(tasks: List[str]) -> None:
        print("\nAvailable Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
