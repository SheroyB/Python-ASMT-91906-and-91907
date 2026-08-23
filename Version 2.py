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