'''This program is the second version of a screentime awareness app,
it uses a Tkinter GUI, a ScreentimeEntry class, and saves data to a JSON file.'''

from tkinter import *
from tkinter import messagebox
import json
import os
from datetime import datetime

data_file = "screentime_log.json"
daily_limit_minutes = 120

class ScreentimeEntry:
    def __init__(self, app, minutes, date, time):
        self.app = app
        self.minutes = minutes
        self.date = date
        self.time = time

    def to_dict(self):
        return {"app": self.app, "minutes": self.minutes, "date": self.date, "time": self.time}

def load_entries():
    if not os.path.exists(data_file):
        return []
    try:
        with open(data_file, "r") as file:
            entries = json.load(file)
        return entries
    except:
        return []

def save_entries(entries):
    with open(data_file, "w") as file:
        json.dump(entries, file)

window = Tk()
window.title("Screentime")
window.geometry("350x350")

window.grid_columnconfigure(0, weight=1)

Label(window, text="Screentime Awareness App", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=(20, 15))

Label(window, text="App or device name:").grid(row=1, column=0)
app_entry = Entry(window, justify="center")
app_entry.grid(row=2, column=0, pady=5)

Label(window, text="Minutes spent:").grid(row=3, column=0)
minutes_entry = Entry(window, justify="center")
minutes_entry.grid(row=4, column=0, pady=5)

status_label = Label(window, text="", font=("Arial", 10))
status_label.grid(row=5, column=0, pady=(15, 0))

sleep_label = Label(window, text="", font=("Arial", 10, "bold"), padx=10, pady=3)
sleep_label.grid(row=6, column=0, pady=(5, 0))

def log_screen_time():
    app_name = app_entry.get().strip()
    minutes_text = minutes_entry.get().strip()

    if not app_name.isalpha():
        messagebox.showerror("Invalid Input", "App name must only contain letters")
        return

    try:
        minutes = int(minutes_text)
    except ValueError:
        messagebox.showerror("Invalid Input", "Minutes must be a whole number")
        return

    if minutes <= 0:
        messagebox.showerror("Invalid Input", "Minutes must be greater than 0")
        return

    now = datetime.now()
    entry = ScreentimeEntry(app_name, minutes, now.strftime("%Y-%m-%d"), now.strftime("%H:%M"))

    entries = load_entries()
    entries.append(entry.to_dict())
    save_entries(entries)

    app_entry.delete(0, END)
    minutes_entry.delete(0, END)

    update_status()

def update_status():
    entries = load_entries()
    today = datetime.now().strftime("%Y-%m-%d")
    total_today = 0
    for saved_entry in entries:
        if saved_entry["date"] == today:
            total_today = total_today + saved_entry["minutes"]

    if total_today > daily_limit_minutes:
        over_by = total_today - daily_limit_minutes
        status_label.config(text=f"Today's total: {total_today}m ({over_by}m over the limit)")
    else:
        remaining = daily_limit_minutes - total_today
        status_label.config(text=f"Today's total: {total_today}m ({remaining}m remaining)")

    if total_today > daily_limit_minutes + 120:
        sleep_label.config(text="High impact on sleep", bg="red")
    elif total_today > daily_limit_minutes:
        sleep_label.config(text="Medium impact on sleep", bg="yellow")
    else:
        sleep_label.config(text="Low impact on sleep", bg="green")