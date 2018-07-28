"""
database.py

Contains functions for interacting with sqlite3

init_directories() -- ensure that any directories that need to exist
do exist

connect() -- connect to database and return db object

store_task(task_data) -- store data about a task in the db

insert_or_update_task(task_name, task_time) -- insert an entry in the database,
or update it if it already exists

table_name() -- generate a table name based on todays date

get_task_time(task) -- return the time spent already on a task today

task_exists(task) -- check if a task exists

ensure_table_exists(name) -- Create table, unless it exists already

get_days() -- return a list of dates when tasks were recorded

get_date_tasks(date) -- return information about tasks done on
a particular day

remove_day(date) -- remove a date's task information from file

class TaskData -- a simple class to hold information on tasks.

"""

# core
import sqlite3
import datetime
import os
import logging

# Directories and files
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data")
DBNAME = os.path.join(DATA_DIR, 'task.db')

# Logging
LOG_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.DEBUG, filename="task.log", format=LOG_FORMAT)

def init_directories():
    """ Create the data directory, if it does not exist already """
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

def connect():
    """ Connect to the local database and return a sqlite3 db object """
    return sqlite3.connect(DBNAME)

def store_task(task_data):
    """
    Provide a TaskData object. These hold the task name,
    as well as the amount of time spent on it.

    If the tasks exists already in todays db table, then
    add the supplied TaskData's time onto it.

    Store the task and its new time in the database.
    """

    # Amount of time spent doing the
    # task passed as arg
    total_time_spent = task_data.time

    # get amount of time spent already doing that
    # task today. It will be None if it has not been
    # done today
    spent_already = get_task_time(task_data.name)

    if not spent_already is None:
        # If it exists, add to total time
        total_time_spent += spent_already[0]


    insert_or_update_task(task_data.name, total_time_spent)

def insert_or_update_task(task_name, task_time):
    """
    Provide the name of a task (string)
    and the time spent on it in minutes (int)

    This stores it in the database. If the task already
    exists, it updates it, otherwise it inserts the new task.
    """

    table = table_name()

    # Create table if it does not exist
    ensure_table_exists(table)

    # Task exists
    if task_exists(task_name):
        cmd = ('''UPDATE ''' + table +
               ''' SET task_time = ? WHERE task_name = ?''')
        values = (task_time, task_name)

    # New task
    else:
        cmd = ('''INSERT INTO ''' +
               table + '''(task_name, task_time) VALUES(?, ?)''')
        values = (task_name, task_time)

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd, values)

    db.close()

def table_name():
    """ Returns a string representing today's date like this: DAY_DD_MM_YYYY """
    d = datetime.datetime.now().date()
    return d.strftime("DAY_%d_%m_%Y")

def get_task_time(task):
    """
    Provide the name of task (string)

    Returns the amount of time taken on it today,
    or None if it doesn't exist.
    """

    task_time = None

    if task_exists(task):

        table = table_name()

        # create tables if they don't exist
        ensure_table_exists(table)

        cmd = ('''SELECT task_time FROM ''' +
               table + ''' WHERE task_name = ?''')

        db = connect()
        with db:
            cursor = db.cursor()
            cursor.execute(cmd, (task, ))
            task_time = cursor.fetchone()

        db.close()

    return task_time

def task_exists(task):
    """
    Supply the name of a task as a string.

    Returns True if it exists in today's table,
    otherwise it returns False
    """

    name = table_name()

    ensure_table_exists(name)

    cmd = ("""SELECT id FROM """ + name +
           """ WHERE task_name = ?""")

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd, (task,))
        entry = cursor.fetchall()
    db.close()

    return len(entry) > 0

def ensure_table_exists(name):
    """
    Supply the name for the table as a string.
    Create the table if it does not already exist
    """

    cmd = ("""CREATE TABLE IF NOT EXISTS """ + name +
           """ (id INTEGER PRIMARY KEY, task_name text, task_time int)""")

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd)

    db.close()

def get_days():
    """
    Returns a list of dates on which tasks were recorded. The dates
    are strings with the format: DD/MM/YYYY. If none exist, the list
    will be empty
    """

    # Query sqlite3 master table, which contains names of all
    # other tables
    cmd = "SELECT name FROM sqlite_master WHERE type='table'"

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd)
        days = cursor.fetchall()

    db.close()

    formatted_days = []

    for d in days:
        dt = datetime.datetime.strptime(d[0], "DAY_%d_%m_%Y")
        formatted_days.append(dt.date().strftime("%d/%m/%Y"))

    return formatted_days

def get_date_tasks(date=None):
    """
    Optionally provide a date as a datetime object. If not provided
    it will default to today's date.

    Returns a list of TaskData objects which hold the name of the
    task and the time spent on it in minutes (see class below)
    """

    if date is None:
        date = datetime.datetime.now()

    cmd = "SELECT * FROM " + date.strftime("DAY_%d_%m_%Y")

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd)
        tasks = cursor.fetchall()

    db.close()

    ret_tasks = []
    for t in tasks:
        ret_tasks.append(TaskData(t[1], t[2]))

    return ret_tasks

def remove_day(date):
    """
    Provide a date as a datetime object

    Remove that date from the database.
    """

    # Dates are represented by tables of tasks
    # with the following format:
    rm_table_name = date.strftime("DAY_%d_%m_%Y")
    # Just drop the table
    cmd = ("""DROP TABLE IF EXISTS """ + rm_table_name)

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd)

    db.close()

class TaskData:
    """
    A simple class to hold data on a task.
    it has two properties:
    name -- any reasonable string, naming a task
    time -- an int for how long was spent on the task,
    in minutes
    """

    def __init__(self, name, time):

        if not isinstance(name, str):
            raise TypeError("TaskData constructor name argument should be a string")
        if not isinstance(time, int):
            raise TypeError("TaskData constructor time argument should be a positive int")
        if time < 0:
            raise ValueError("TaskData time should non-negative")

        self.name = name
        self.time = time

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        same_class = isinstance(other, TaskData)
        return same_class and self.__dict__ == other.__dict__
        