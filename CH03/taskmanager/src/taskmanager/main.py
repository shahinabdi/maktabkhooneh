import json
import time
from datetime import datetime

tasks = {}
current_task = None
start_time = None
end_time = None
duration = None

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
            continue
        task_name = input("Enter task name: ")
        start_time = time.time()
        current_task = task_name
        print(f"Task {task_name} started!")

        if task_name not in tasks:
            tasks[task_name] = {"total_time": 0, "sessions": []}
    elif choice == "2":
        if current_task == None:
            print("Error: No task running!")
            continue

        end_time = time.time()

        duration = end_time - start_time

        tasks[current_task]["total_time"] += duration
        tasks[current_task]["sessions"].append(
            {
                "start": datetime.fromtimestamp(start_time).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "end": datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S"),
                "duration": duration,
            }
        )

        try:
            f = open("tasks.json", "w")
            json.dump(tasks, f)
            f.close()
        except:
            print("Error: Saving data was unsuccessful!")

        print(f"Task '{current_task}' stopped! Duration: {duration:.2f} seconds")

        current_task = None
        start_time = None
    elif choice == "5":
        break
# 2. Stop task
# 3. View tasks
# 4. Delete task
