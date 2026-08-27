'''This program is the third version of a screentime awareness app,
it uses a Tkinter GUI, a ScreentimeEntry class, and saves data to a JSON file.
This version adds a per-app breakdown and finds the dominant app for today.'''

from tkinter import *
from tkinter import messagebox
import json
import os
from datetime import datetime

data_file = "screentime_log.json" # Name of the file that stores all saved entries
daily_limit_minutes = 120 # General daily screentime guideline used for comparison

class ScreentimeEntry:
    # Represents one logged screentime entry, bundling all its data together
    def __init__(self, app, minutes, date, time):
        self.app = app # The name of the app or device used, e.g. "YouTube"
        self.minutes = minutes # How many minutes were spent on it
        self.date = date # The date this entry was logged, e.g. "2026-08-21"
        self.time = time # The time this entry was logged, e.g. "21:45"

    def to_dict(self): # Turns the object into a dictionary so it can be saved as JSON
        return {"app": self.app, "minutes": self.minutes, "date": self.date, "time": self.time}

def load_entries():
    # Reads all saved entries from the JSON file, returns an empty list if none exist
    if not os.path.exists(data_file): # If the file has never been created yet
        return []
    try:
        with open(data_file, "r") as file:
            entries = json.load(file) # Turns the JSON text back into a list of dictionaries
        return entries
    except: # Handles a missing or corrupted file without crashing
        return []

def save_entries(entries):
    # Writes the full list of entries back to the JSON file, overwriting what was there before
    with open(data_file, "w") as file:
        json.dump(entries, file)

window = Tk()
window.title("Screentime")
window.geometry("350x420")

window.grid_columnconfigure(0, weight=1) # Lets column 0 stay centred as the window resizes

Label(window, text="Screentime Awareness App", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=(20, 15))

Label(window, text="App or device name:").grid(row=1, column=0)
app_entry = Entry(window, justify="center") # justify="center" centres the typed text itself
app_entry.grid(row=2, column=0, pady=5)

Label(window, text="Minutes spent:").grid(row=3, column=0)
minutes_entry = Entry(window, justify="center")
minutes_entry.grid(row=4, column=0, pady=5)

status_label = Label(window, text="", font=("Arial", 10)) # Starts empty, filled in by update_status()
status_label.grid(row=5, column=0, pady=(15, 0))

sleep_label = Label(window, text="", font=("Arial", 10, "bold"), padx=10, pady=3) # Coloured badge
sleep_label.grid(row=6, column=0, pady=(5, 0))

breakdown_label = Label(window, text="", font=("Arial", 9), justify="center")
breakdown_label.grid(row=7, column=0, pady=(15, 0))

dominant_label = Label(window, text="", font=("Arial", 9, "bold"))
dominant_label.grid(row=8, column=0, pady=(5, 0))

def log_screen_time():
    # Validates the form, creates a ScreentimeEntry, saves it, then updates the labels
    app_name = app_entry.get().strip() # .strip() removes accidental leading/trailing spaces
    minutes_text = minutes_entry.get().strip() # Entry boxes always return text, never numbers

    if not app_name.isalpha(): # .isalpha() checks every character is a letter, no spaces/numbers
        messagebox.showerror("Invalid Input", "App name must only contain letters")
        return # Stops the function here so a bad entry never gets saved

    try:
        minutes = int(minutes_text) # Tries to turn the typed text into a whole number
    except ValueError: # Runs if int() fails, e.g. the box was blank or had letters in it
        messagebox.showerror("Invalid Input", "Minutes must be a whole number")
        return

    if minutes <= 0: # Checks that user entered a number greater than 0
        messagebox.showerror("Invalid Input", "Minutes must be greater than 0")
        return

    now = datetime.now() # The exact date and time right now
    # strftime formats the date/time into text, "%Y-%m-%d" gives e.g. "2026-08-21", "%H:%M" gives "21:45"
    entry = ScreentimeEntry(app_name, minutes, now.strftime("%Y-%m-%d"), now.strftime("%H:%M"))

    entries = load_entries() # Load what's already saved so we don't overwrite old entries
    entries.append(entry.to_dict()) # Add the new entry to the list
    save_entries(entries) # Write the whole updated list back to the file

    app_entry.delete(0, END) # Clears the text boxes so they're empty for the next entry
    minutes_entry.delete(0, END)

    update_status() # Refresh the labels now that a new entry has been saved

def update_status():
    # Works out today's total minutes and updates the status and sleep labels
    entries = load_entries() # Load whatever is currently saved, could be empty or have old data
    today = datetime.now().strftime("%Y-%m-%d") # Today's date as text, so it matches saved entries
    total_today = 0
    app_totals = {}
    for saved_entry in entries: # Goes through every saved entry, from every day
        if saved_entry["date"] == today: # Only counts the ones that match today's date
            total_today = total_today + saved_entry["minutes"]
            app = saved_entry["app"]
            if app in app_totals:
                app_totals[app] = app_totals[app] + saved_entry["minutes"]
            else:
                app_totals[app] = saved_entry["minutes"]

    if total_today > daily_limit_minutes:
        over_by = total_today - daily_limit_minutes
        # f-strings let you drop variables straight into text using { }
        status_label.config(text=f"Today's total: {total_today}m ({over_by}m over the limit)")
    else:
        remaining = daily_limit_minutes - total_today
        status_label.config(text=f"Today's total: {total_today}m ({remaining}m remaining)")

    # Checked in order: furthest over the limit first, since a number can only match one of these
    if total_today > daily_limit_minutes + 120: # More than 120 minutes over the limit
        sleep_label.config(text="High impact on sleep", bg="red")
    elif total_today > daily_limit_minutes: # Over the limit, but not by that much
        sleep_label.config(text="Medium impact on sleep", bg="yellow")
    else: # At or under the daily limit
        sleep_label.config(text="Low impact on sleep", bg="green")
    breakdown_text = ""
    for app in app_totals:
        breakdown_text = breakdown_text + app + " " + str(app_totals[app]) + "m\n"
    breakdown_label.config(text=breakdown_text)

Button(window, text="Log Screen Time", command=log_screen_time).grid(row=9, column=0, pady=15)

update_status() # Runs once on startup so the labels are correct even before logging anything new

window.mainloop() # Keeps the window open and listening for clicks until it's closed