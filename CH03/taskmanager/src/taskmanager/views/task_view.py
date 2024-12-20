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
