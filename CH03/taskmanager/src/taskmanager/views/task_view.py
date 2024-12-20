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

    @staticmethod
    def show_task_options() -> None:
        print("\nView Options:")
        print("1. Basic Info")
        print("2. All Sessions")
        print("3. Last 3 Sessions")
        print("4. Back Main Menu")

    @staticmethod
    def show_task_details(task_name: str, task_data: Dict, view_type: str) -> None:
        print(f"\nTask: {task_name}")
        print(f"Total time: {task_data['total_time']:.2f} seconds")
        print(f"Number of sessions: {len(task_data['sessions'])}")

        if view_type in ["2", "3"]:
            sessions = task_data["sessions"]
            if view_type == "3":
                sessions = sessions[-3:]

            print("\nSessions:")
            print("=" * 4)
            for session in sessions:
                print(f"Start: {session['start']}")
                print(f"End: {session['end']}")
                print(f"Duration: {session['duration']:.2f} seconds")
                print("-" * 40)
