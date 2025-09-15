import json
import os
import time
from datetime import datetime
from plyer import notification

FILE_REMINDER = os.path.join(os.path.dirname(__file__), "reminders.json")

def load_reminder():
    try:
        with open(FILE_REMINDER, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_reminder(reminders):
    with open(FILE_REMINDER, "w") as file:
        json.dump(reminders, file, indent=2)

def add_reminder(text, due):
    reminders = load_reminder()
    reminders.append({"text": text, "due_time": due})
    save_reminder(reminders)

def show_reminder():
    reminders = load_reminder()
    if not reminders:
        return "No reminders set."
    lines = ["Reminders:"]
    for i, rem in enumerate(reminders):
        try:
            time_str = datetime.fromtimestamp(rem["due_time"]).strftime("%Y-%m-%d %H:%M")
        except Exception:
            time_str = "Unknown time"
        lines.append(f"{i+1}. [{time_str}] {rem['text']}")
    return "\n".join(lines)

def check_reminder():
    reminders = load_reminder()
    now = time.time()
    due_list, future_list = [], []
    for rem in reminders:
        if rem["due_time"] <= now:
            due_list.append(rem)
        else:
            future_list.append(rem)
    save_reminder(future_list)
    return due_list

def reminder_notif_loop():
    while True:
        due_list = check_reminder()
        if due_list:
            for rem in due_list:
                notification.notify(
                    title="Reminder",
                    message=rem["text"],
                    timeout=10
                )
                print(f"\n🔔 REMINDER: {rem['text']}")
        time.sleep(30)
