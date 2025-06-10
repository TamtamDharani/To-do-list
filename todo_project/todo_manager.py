import json
import os
import csv
from datetime import datetime, timedelta

TASKS_FILE = "tasks.json"
CSV_FILE = "tasks.csv"

# Load tasks from JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Add a new task with priority
def add_task():
    tasks = load_tasks()
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
    priority = input("Enter priority (low, medium, high) or leave blank: ").lower()
    if priority not in ["low", "medium", "high"]:
        priority = "low"  # default priority

    task = {
        "description": description,
        "due_date": due_date if due_date else None,
        "completed": False,
        "priority": priority
    }
    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully!\n")

# Add task from web (no input(), just parameters)
def add_task_web(description, due_date, priority):
    tasks = load_tasks()
    if priority not in ["low", "medium", "high"]:
        priority = "low"
    task = {
        "description": description,
        "due_date": due_date if due_date else None,
        "completed": False,
        "priority": priority
    }
    tasks.append(task)
    save_tasks(tasks)

# View tasks with optional filters and show reminders for due soon
def view_tasks(filter_type="all"):
    tasks = load_tasks()
    print("\n📋 Your Tasks:")
    today = datetime.today()
    found = False

    for i, task in enumerate(tasks):
        due = task["due_date"]
        show = False

        if filter_type == "all":
            show = True
        elif filter_type == "completed" and task["completed"]:
            show = True
        elif filter_type == "pending" and not task["completed"]:
            show = True
        elif filter_type == "due_soon" and due:
            due_date = datetime.strptime(due, "%Y-%m-%d")
            if 0 <= (due_date - today).days <= 3 and not task["completed"]:
                show = True

        if show:
            found = True
            status = "✅" if task["completed"] else "❌"
            due_display = f" (Due: {due})" if due else ""
            priority_display = f" [Priority: {task.get('priority', 'low').capitalize()}]"
            print(f"{i+1}. {status} {task['description']}{due_display}{priority_display}")

            # Reminder if due today or tomorrow and not completed
            if not task["completed"] and due:
                due_date = datetime.strptime(due, "%Y-%m-%d")
                days_left = (due_date - today).days
                if 0 <= days_left <= 1:
                    print("   🔔 Reminder: Task due very soon!")

    if not found:
        print("No tasks to display for this filter.")
    print()

# Mark a task as completed
def mark_task_completed():
    tasks = load_tasks()
    view_tasks("pending")
    try:
        task_num = int(input("Enter task number to mark as completed: ")) - 1
        if 0 <= task_num < len(tasks):
            tasks[task_num]["completed"] = True
            save_tasks(tasks)
            print("✅ Task marked as completed!\n")
        else:
            print("⚠️ Invalid task number.\n")
    except ValueError:
        print("⚠️ Please enter a valid number.\n")

# Edit a task including priority
def edit_task():
    tasks = load_tasks()
    view_tasks()
    try:
        task_num = int(input("Enter task number to edit: ")) - 1
        if 0 <= task_num < len(tasks):
            new_desc = input("Enter new description (leave blank to keep current): ")
            new_due = input("Enter new due date (YYYY-MM-DD) or leave blank: ")
            new_priority = input("Enter new priority (low, medium, high) or leave blank: ").lower()

            if new_desc:
                tasks[task_num]["description"] = new_desc
            if new_due:
                tasks[task_num]["due_date"] = new_due
            if new_priority in ["low", "medium", "high"]:
                tasks[task_num]["priority"] = new_priority

            save_tasks(tasks)
            print("✏️ Task updated successfully!\n")
        else:
            print("⚠️ Invalid task number.\n")
    except ValueError:
        print("⚠️ Please enter a valid number.\n")