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
# 2. Stop task
# 3. View tasks
# 4. Delete task
