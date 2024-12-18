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

# 1. Start task
if current_task != None:
    print("Error: One task already running!")
task_name = input("Enter task name: ")
start_time = time.time()
print(f"Task {task_name} started!")

if task_name not in tasks:
    tasks[task_name] = {"total_time": 0, "sessions": []}
# 2. Stop task
# 3. View tasks
# 4. Delete task
