'''This program is the second version of a screentime awareness app,
it uses a Tkinter GUI, a ScreentimeEntry class, and saves data to a JSON file.'''

from tkinter import *
from tkinter import messagebox
import json
import os
from datetime import datetime

data_file = "screentime_log.json"
daily_limit_minutes = 120