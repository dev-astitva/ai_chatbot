import threading
import time
import re
from plyer import notification
from reminders import add_reminder, show_reminder, check_reminder, load_reminder, save_reminder
from todo import add_todo, show_todo, finish_todo, remove_todo, load_todo, save_todo
from gemini import chat_gemini
from config import load_conf, save_conf
from news import get_news
from weather import get_weather

user_conf = load_conf()
chat_log = []

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear_screen()
    print("==== AI Assistant ====")
    print("Options:")
    print("[1] Chat")
    print("[2] Set Reminder")
    print("[3] Show Reminders")
    print("[4] Get News")
    print("[5] Weather")
    print("[6] To-Do List")
    print("[7] Preferences")
    print("[0] Exit")

def reminder_loop():
    while True:
        due_list = check_reminder()
        if due_list:
            for rem in due_list:
                notification.notify(
                    title="Reminder",
                    message=rem['text'],
                    timeout=10
                )
                print(f"\n🔔 REMINDER: {rem['text']}")
        time.sleep(30)

def set_reminder():
    rem_text = input("What should I remind you of? ")
    rem_mins = input("In how many minutes? ")
    try:
        rem_mins = int(rem_mins)
        rem_time = time.time() + rem_mins * 60
        add_reminder(rem_text, rem_time)
        print("Reminder added!")
    except Exception:
        print("Invalid input.")

def preferences_menu():
    print("\n[Preferences]")
    print("[1] Google Gemini API key")
    print("[2] NewsAPI key")
    print("[3] Weather API key")
    print("[4] News topics")
    pref_choice = input("Choose option: ")
    if pref_choice == '1':
        user_conf["google_api_key"] = input("Enter Google Gemini API key: ")
    elif pref_choice == '2':
        user_conf["news_api_key"] = input("Enter NewsAPI key: ")
    elif pref_choice == '3':
        user_conf["weather_api_key"] = input("Enter Weather API key: ")
    elif pref_choice == '4':
        user_conf["news_prefs"] = input("News topics (comma separated): ")
    save_conf(user_conf)
    print("Preferences updated.")

def parse_rem_cmd(text):
    match = re.search(
        r"add (?:a )?reminder for (.+?) (?:in|after) (\d+) min",
        text, re.IGNORECASE
    )
    if match:
        rem_text = match.group(1).strip()
        rem_mins = int(match.group(2))
        return rem_text, rem_mins
    return None

def parse_todo_cmd(text):
    match = re.search(r"add (?:a )?to[- ]?do(?: task)? (.+)", text, re.IGNORECASE)
    if match:
        todo_text = match.group(1).strip()
        return todo_text
    return None

def parse_rem_remove_cmd(text):
    match = re.search(r"remove (?:the )?reminder (\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(1)) - 1
    return None

def parse_todo_remove_cmd(text):
    match = re.search(r"remove (?:the )?(?:task|todo|to-?do) (\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(1)) - 1
    return None

def chat_menu():
    print("\nStart chatting with your assistant. Type 'back' to return.")
    while True:
        user_text = input("You: ").strip()
        if user_text.lower() == "back":
            break
        rem_cmd = parse_rem_cmd(user_text)
        if rem_cmd:
            rem_text, rem_mins = rem_cmd
            from time import time as now
            add_reminder(rem_text, now() + rem_mins * 60)
            print(f"Assistant: Reminder added for '{rem_text}' in {rem_mins} minutes.")
            print("Current reminders stored:")
            print(show_reminder())
            continue
        todo_cmd = parse_todo_cmd(user_text)
        if todo_cmd:
            add_todo(todo_cmd)
            print(f"Assistant: To-Do task '{todo_cmd}' added.")
            print("Current to-dos stored:")
            print(show_todo())
            continue
        rem_rem_idx = parse_rem_remove_cmd(user_text)
        if rem_rem_idx is not None:
            rem_list = load_reminder()
            if 0 <= rem_rem_idx < len(rem_list):
                removed = rem_list.pop(rem_rem_idx)
                save_reminder(rem_list)
                print(f"Assistant: Removed reminder '{removed['text']}'.")
            else:
                print("Assistant: Invalid reminder number.")
            continue
        todo_rem_idx = parse_todo_remove_cmd(user_text)
        if todo_rem_idx is not None:
            td_list = load_todo()
            if 0 <= todo_rem_idx < len(td_list):
                removed = td_list.pop(todo_rem_idx)
                save_todo(td_list)
                print(f"Assistant: Removed to-do task '{removed['task']}'.")
            else:
                print("Assistant: Invalid to-do number.")
            continue
        if re.search(r"(show|list) reminders", user_text, re.IGNORECASE):
            rem_list = show_reminder()
            print(f"Assistant:\n{rem_list}")
            continue
        if re.search(r"(show|list) to-?dos?", user_text, re.IGNORECASE):
            to_list = show_todo()
            print(f"Assistant:\n{to_list}")
            continue
        resp = chat_gemini(user_text)
        print(f"Assistant: {resp}")

def news_menu():
    print("\nFetching news...\n")
    pref = user_conf.get("news_prefs", "technology")
    news = get_news(pref)
    print(news)

def weather_menu():
    city = input("Enter city name: ")
    print(get_weather(city))

def todo_menu():
    while True:
        print("\n[To-Do Menu]")
        print("[1] Add To-Do")
        print("[2] Show To-Dos")
        print("[3] Finish To-Do")
        print("[4] Remove To-Do")
        print("[0] Back")
        choice = input("Select option: ")
        if choice == "1":
            task = input("Task: ")
            add_todo(task)
            print("Added.")
        elif choice == "2":
            print(show_todo())
        elif choice == "3":
            print(show_todo())
            idx = input("Task number to finish: ")
            try:
                print(finish_todo(int(idx) - 1))
            except Exception:
                print("Invalid input.")
        elif choice == "4":
            print(show_todo())
            idx = input("Task number to remove: ")
            try:
                print(remove_todo(int(idx) - 1))
            except Exception:
                print("Invalid input.")
        elif choice == "0":
            break
        else:
            print("Invalid input.")

def main():
    threading.Thread(target=reminder_loop, daemon=True).start()
    while True:
        main_menu()
        choice = input("Choose option: ")
        if choice == "1":
            chat_menu()
        elif choice == "2":
            set_reminder()
        elif choice == "3":
            print(show_reminder())
            input("Press Enter to return...")
        elif choice == "4":
            news_menu()
            input("Press Enter to return...")
        elif choice == "5":
            weather_menu()
            input("Press Enter to return...")
        elif choice == "6":
            todo_menu()
        elif choice == "7":
            preferences_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
