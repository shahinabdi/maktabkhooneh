import json
from datetime import datetime
from typing import Dict, List, Optional


class TaskModel:
    def __init__(self, filename: str = "tasks.json"):
        pass

    def load_tasks(self) -> None:
        pass

    def save_tasks(self) -> None:
        pass

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
