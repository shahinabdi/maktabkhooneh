import json
from datetime import datetime
from typing import Dict, List, Optional


class TaskModel:
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: Dict = {}
        self.current_task: Optional[str] = None
        self.start_time: Optional[float] = None
        self.load_tasks()

    def load_tasks(self) -> None:
        try:
            with open(self.filename, "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = {}
        except json.JSONDecodeError:
            raise Exception("Invalid JSON format in tasks file")

    def save_tasks(self) -> None:
        try:
            with open(self.filename, "w") as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            raise Exception(f"Error saving tasks: {str(e)}")

    def start_task(self, task_name: str) -> None:
        if self.current_task is not None:
            raise Exception("One task is already running!")

        normalized_task_name = task_name.strip().lower()
        if not normalized_task_name:
            raise Exception("Task name cannot be empty")

        self.start_time = datetime.now().timestamp()
        self.current_task = normalized_task_name

        if normalized_task_name not in self.tasks:
            self.tasks[normalized_task_name] = {"total_time": 0, "sessions": []}

    def stop_task(self) -> Dict:
        if self.current_task is None:
            raise Exception("No task is currently running")

        end_time = datetime.now().timestamp()
        duration = end_time - self.start_time

        task_data = self.tasks[self.current_task]
        task_data["total_time"] += duration

        session = {
            "start": datetime.fromtimestamp(self.start_time).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "end": datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S"),
            "duration": duration,
        }

        task_data["sessions"].append(session)
        self.save_tasks()

        result = {
            "task_name": self.current_task,
            "duration": duration,
            "session": session,
        }

        self.current_task = None
        self.start_time = None
        return result

    def delete_task(self, task_name: str) -> None:
        normalized_task_name = task_name.strip().lower()

        if normalized_task_name not in self.tasks:
            raise Exception("Task not found")

        del self.tasks[normalized_task_name]
        self.save_tasks()

    def get_current_task(self) -> Optional[str]:
        return self.current_task

    def get_all_tasks(self) -> List[str]:
        return sorted(list(self.tasks.keys()))

    def get_task_details(self, task_name: str) -> Dict:
        normalized_task_name = task_name.strip().lower()

        if normalized_task_name not in self.tasks:
            raise Exception("Task not found")
        return self.tasks[normalized_task_name]
