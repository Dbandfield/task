import sqlite3
import datetime
import os
import logging

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data")
DBNAME = os.path.join(DATA_DIR, 'task.db')

LOG_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.DEBUG, filename="task.log", format=LOG_FORMAT)

def initDirectories():
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

def connect():
    return sqlite3.connect(DBNAME)

def storeTask(taskData):

    # Amount of time spent doing the 
    # task passed as arg
    totalTimeSpent = taskData.time

    # get amount of time spent already doing that
    # task today. It will be None if it has not been
    # done today
    spentAlready = getTaskTime(taskData.name)

    if not spentAlready is None:
        # If it exists, add to total time
        totalTimeSpent += spentAlready[0]


    insertOrUpdateTask(taskData.name, totalTimeSpent)

def insertOrUpdateTask(taskName, taskTime):
    
    table = tableName()

    ensureTableExists(table)

    if taskExists(taskName):
        cmd = ('''UPDATE ''' + table + 
                ''' SET taskTime = ? WHERE taskName = ?''')
        values = (taskTime, taskName)
        

    else:
        cmd = ('''INSERT INTO ''' + 
            table + '''(taskName, taskTime) VALUES(?, ?)''')
        values = (taskName, taskTime)

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd, values)

    db.close()     

def tableName():
    d = datetime.datetime.now().date()
    return d.strftime("DAY_%d_%m_%Y")

def getTaskTime(task):

    taskTime = None

    if taskExists(task):

        table = tableName()

        ensureTableExists(table)

        cmd = ('''SELECT taskTime FROM ''' + 
            table + ''' WHERE taskName = ?''')

        db = connect()
        with db:
            cursor = db.cursor()
            cursor.execute(cmd, (task, ))
            taskTime = cursor.fetchone()

        db.close()

    return taskTime

def taskExists(task):

    name = tableName()

    ensureTableExists(name)

    cmd = ("""SELECT id FROM """ + name + 
          """ WHERE taskName = ?""") 

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd, (task,))
        entry = cursor.fetchall()
    db.close()

    return len(entry) > 0

def ensureTableExists(name):
    cmd = ("""CREATE TABLE IF NOT EXISTS """ + name + 
           """ (id INTEGER PRIMARY KEY, taskName text, taskTime int)""")

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd)

    db.close()

def getDays():
    cmd = "SELECT name FROM sqlite_master WHERE type='table'"

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd)
        days = cursor.fetchall()

    db.close()

    formattedDays = []

    for d in days:
        dt = datetime.datetime.strptime(d[0], "DAY_%d_%m_%Y")
        formattedDays.append(dt.date().strftime("%d/%m/%Y"))

    return formattedDays

def getDateTasks(date=None):

    if date is None:
        date = datetime.datetime.now()

    cmd = "SELECT * FROM " + date.strftime("DAY_%d_%m_%Y")

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd)
        tasks = cursor.fetchall()

    db.close()

    retTasks = []
    for t in tasks:
        retTasks.append(TaskData(t[1], t[2]))

    return retTasks

def removeDay(date):
    tableName = date.strftime("DAY_%d_%m_%Y")
    cmd = ("""DROP TABLE IF EXISTS """ + tableName)

    db = connect()
    with db:
        cursor = db.cursor()
        cursor.execute(cmd)

    db.close()

class TaskData:

    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        sameClass = isinstance(other, TaskData)
        return sameClass and self.__dict__ == other.__dict__




