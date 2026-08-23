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