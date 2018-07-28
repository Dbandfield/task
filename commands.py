"""
commands.py

This contains the bulk of the logic for executing the
commands. Curses and sqlite3 specifics are kept in
separate files (display.py and database.py respectively).

get_minutes_seconds(seconds_in) -- convert seconds to minutes and seconds
make_time_string(seconds_in) -- convert seconds to a string of minutes and seconds
start(task_name) -- displays countdown for task and handles user input
ls() -- prints out the date of day where a task has been recorded
show(date_str) -- shows information on tasks done for a specified day
rm(date_str) -- removes all information about a particular day
"""

# core
from time import sleep
import sys
from datetime import datetime
import logging

# project
import display
import database

# Logging
LOG_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.DEBUG, filename="task.log", format=LOG_FORMAT)

def get_minutes_seconds(seconds_in):
    """
    Provide seconds as an integer.

    Convert to minutes and remainder seconds,
    returned as two separate integers
    """

    minutes = int(seconds_in/60)
    seconds_out = int(seconds_in % 60)

    return minutes, seconds_out

def make_time_string(seconds_in):
    """
    Provide seconds as an integer.

    Returns a string representing that number as minutes
    and remainder seconds. If minutes is 0 then just seconds
    will be shown
    """

    minutes, seconds = get_minutes_seconds(seconds_in)

    if minutes == 0:
        minString = ""
    elif minutes == 1:
        minString = str(minutes) + " minute and "
    else:
        minString = str(minutes) + " minutes and "

    return minString + str(seconds) + " seconds"

def start(task_name):
    """
    Display a timer counting up in minutes.
    Handle controls for when the user wants to store the task, exit without
    storing, or pause

    task_name -- a user defined string to identify task
    """

    # ensure directories exist
    database.init_directories()

    # To keep track of time spent
    last_time = 0
    delta = 0
    timer = 0

    # Create text elements
    header = "You have been doing " + task_name + " for "
    header_text = display.TextElement(header, 0)
    date_text = "0"
    time_text = display.TextElement(date_text, 1)
    break1 = display.TextElement("", 2)
    status = display.TextElement("RECORDING", 3)
    break2 = display.TextElement("", 4)

    # user control information
    instr_text_enter = "Press ENTER to end task and save"
    instr_text_p = "Press p to pause task"
    instr_text_q = "Press q to exit without saving task"
    instr1 = display.TextElement(instr_text_enter, 5)
    instr2 = display.TextElement(instr_text_p, 6)
    instr3 = display.TextElement(instr_text_q, 7)

    elements = [header_text, time_text, break1, status, break2, instr1, instr2, instr3]
    elements.sort()

    screen = display.init_display()

    display.update(screen, elements)

    paused = False

    last_time = datetime.now()

    # will loop until user exit
    while True:

        delta = datetime.now() - last_time
        last_time = datetime.now()
        if not paused:
            timer += delta.total_seconds()

        time_text.txt = make_time_string(timer)

        # Update the text
        display.update(screen, elements)

        # Get user input, if any
        inp = display.run(screen)

        if inp in ('q', 'Q'):
            display.end(screen)
            sys.exit(0)
        elif inp in ('p', 'P'):
            if paused:
                status.txt = 'RECORDING'
                paused = False
            else:
                status.txt = 'PAUSED'
                paused = True
        # ENTER key could be any one of these based on system
        elif inp in ('KEY_ENTER', '\n', '\r'):

            # Commit to file
            task_obj = database.TaskData(task_name, timer)
            database.store_task(task_obj)
            display.end(screen)
            sys.exit(0)

        # Let's not overwork the CPU
        sleep(0.01)

    display.end(screen)

def ls():
    """
    Print out the dates of every day when a task was recorded

    Unlike start and show, this does not use curses
    """

    # Ensure directories exist
    database.init_directories()

    days = database.get_days()

    for d in days:
        print(d)

def show(date_str=None):
    """
    Shows each task done on a day and the total time spent
    doing it. Multiple recordings of the same task are
    cumulative.

    date_str -- a string in the format DD/MM/YYYY of the day to show. If
    not supplied, it defaults to today.
    """

    # ensure directories exist
    database.init_directories()

    if date_str is None:
        # Today
        date = datetime.now().date()
    else:
        try:
            date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as err:
            print("Date format must be as follows: DD/MM/YYYY")
            sys.exit(1)

    today = date == datetime.now().date()

    tasks = database.get_date_tasks(date)

    # Will hold text elements
    elements = []
    # Lower priority elements will be further up the screen
    prio = 0

    # Context sensitive header
    if today:
        header_start = "Today "
    else:
        header_start = "On " + date.strftime("%d/%m/%Y") + " "

    # there are tasks to display
    if len(tasks) > 0:
        header = header_start + "you did the following tasks: "
    # there are no tasks to display
    else:
        header = header_start + "you did no tasks."

    header_text = display.TextElement(header, prio)
    prio += 1
    elements.append(header_text)

    break1 = display.TextElement("", prio)
    prio += 1
    elements.append(break1)

    # get total time spent on all tasks
    total_time = sum([t.time for t in tasks])

    for t in tasks:
        # Time taken as percentage of total
        # spent on all tasks this day
        percent = round(t.time / total_time * 100)

        txt = t.name + " for "
        txt += make_time_string(t.time)
        txt += " - " + str(percent) + "%"
        elements.append(display.TextElement(txt, prio))
        prio += 1

    break2 = display.TextElement("", prio)
    prio += 1
    elements.append(break2)

    instr_text_enter = "Press q or ENTER to exit"
    instr1 = display.TextElement(instr_text_enter, prio)
    elements.append(instr1)

    elements.sort()

    screen = display.init_display()

    display.update(screen, elements)

    # loop until user quits
    while True:

        display.update(screen, elements)

        inp = display.run(screen)

        if inp in ('KEY_ENTER', '\n', '\r', 'q', 'Q'):
            display.end(screen)
            sys.exit(0)

        # Lets not overwork the CPU
        sleep(0.01)

    display.end(screen)

def rm(date_str):
    """
    Removes information for a particular day.

    date_str - a string of the format DD/MM/YY indicating
    which day to remove
    """
    database.init_directories()

    try:
        date = datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError as err:
        print("Date format must be as follows: DD/MM/YYYY")
        sys.exit(1)

    database.remove_day(date)