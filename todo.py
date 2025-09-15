import json
import os

FILE_TODO = os.path.join(os.path.dirname(__file__), "todos.json")

def load_todo():
    try:
        with open(FILE_TODO, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_todo(todos):
    with open(FILE_TODO, "w") as file:
        json.dump(todos, file, indent=2)

def add_todo(task):
    todos = load_todo()
    todos.append({"task": task, "completed": False})
    save_todo(todos)

def show_todo():
    todos = load_todo()
    if not todos:
        return "No to-do tasks."
    lines = ["To-Dos:"]
    for i, todo in enumerate(todos):
        status = "✓" if todo.get("completed", False) else "✗"
        lines.append(f"{i+1}. [{status}] {todo['task']}")
    return "\n".join(lines)

def finish_todo(index):
    todos = load_todo()
    if 0 <= index < len(todos):
        todos[index]["completed"] = True
        save_todo(todos)
        return f"Task {index+1} marked complete."
    else:
        return "Invalid task number."

def remove_todo(index):
    todos = load_todo()
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        save_todo(todos)
        return f"Deleted task: {removed['task']}"
    else:
        return "Invalid task number."
