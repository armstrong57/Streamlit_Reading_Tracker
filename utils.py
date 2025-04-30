import datetime
import calendar
import numpy as np

def np_to_datetime(date):
    """
    Converts a numpy datetime64 object to a python datetime object 
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    """
    timestamp = ((date - np.datetime64('1970-01-01T00:00:00'))
                 / np.timedelta64(1, 's'))
    return datetime.utcfromtimestamp(timestamp)

def calculate_year_percent(date):
    # Calculate the percentage of the year completed to 'date'

    # Calculate the percentage from completed months
    days_done = date.day
    if date.month != 1:
        for month in range(date.month - 1):
            days_done += calendar.monthrange(date.year, month + 1)[1]

    # Calculate the percentage from the current partial month, 
    if calendar.isleap(date.year):
        percent_done = float(days_done) / 366.0
    else:
        percent_done = float(days_done) / 365.0
    
    return percent_done