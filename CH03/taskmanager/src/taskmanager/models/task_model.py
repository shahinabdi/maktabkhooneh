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
        pass

    def stop_task(self) -> Dict:
        pass

    def delete_task(self, task_name: str) -> None:
        pass

    def get_current_task(self) -> Optional[str]:
        pass

    def get_all_tasks(self) -> List[str]:
        pass

    def get_taks_details(self, task_name: str) -> Dict:
        pass
