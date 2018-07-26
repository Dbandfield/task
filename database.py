import sqlite3
import datetime
import logging

DBNAME = "data/task.db"

LOG_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.DEBUG, filename="task.log", format=LOG_FORMAT)

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

class TaskData:

    def __init__(self, name, time):
        self.name = name
        self.time = time




