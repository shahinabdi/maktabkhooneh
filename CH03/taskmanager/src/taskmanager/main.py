import json
import time
from datetime import datetime

tasks = {}
current_task = None
start_time = None
Duration = None

# Load
try:
    f = open("tasks.json", "r")
    tasks = json.load(f)
    f.close()
except:
    tasks = {}

while True:
    # Menu
    print("\n1. Start task")
    print("2. Stop task")
    print("3. View task")
    print("4. Delete task")
    print("5. Exit")

    choice = input("Choose option: ")
    if choice == "1":
        # 1. Start task
        if current_task != None:
            print("Error: One task already running!")
        task_name = input("Enter task name: ")
        start_time = time.time()
        print(f"Task {task_name} started!")

        if task_name not in tasks:
            tasks[task_name] = {"total_time": 0, "sessions": []}
    elif choice == "5":
        break
# 2. Stop task
# 3. View tasks
# 4. Delete task
