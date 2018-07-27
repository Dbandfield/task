import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database
import pytest
import mock
import sqlite3
import datetime

def test_initDirectories(tmpdir):

    temp = tmpdir.mkdir("tmp")
    newDir = os.path.join(temp, 'new')
    database.DATA_DIR = newDir
    database.initDirectories()
    assert os.path.isdir(newDir)

def test_connect(tmpdir):

    temp = tmpdir.mkdir("tmp")
    newDir = os.path.join(temp, 'new')
    database.DATA_DIR = newDir
    db = database.connect()
    assert type(db) is sqlite3.Connection

def test_storeTask(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    testData = database.TaskData('TEST', 10)
    expected = (1, 'TEST', 10)

    database.storeTask(testData)

    # Now check database
    checkPath = os.path.join(temp, "task.db")
    checkDB = sqlite3.connect(checkPath)
    checkTable = database.tableName()
    checkCMD = ("""SELECT id, taskName, taskTime FROM """ + 
                checkTable)
    with checkDB:
        cursor = checkDB.cursor()
        cursor.execute(checkCMD)
        res = cursor.fetchall()
    checkDB.close()

    assert res[0] == expected

def test_insertOrUpdateTask_insert(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    testName = "TEST"
    testTime = 10
    expected = (1, 'TEST', 10)

    database.insertOrUpdateTask(testName, testTime)

    # Now check database
    checkPath = os.path.join(temp, "task.db")
    checkDB = sqlite3.connect(checkPath)
    checkTable = database.tableName()
    checkCMD = ("""SELECT id, taskName, taskTime FROM """ + 
                checkTable)
    with checkDB:
        cursor = checkDB.cursor()
        cursor.execute(checkCMD)
        res = cursor.fetchall()
    checkDB.close()

    assert res[0] == expected

def test_insertOrUpdateTask_update(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    testName = "TEST"
    testTime = 10
    testTimeUpdate = 11
    expected = (1, 'TEST', 11)

    database.insertOrUpdateTask(testName, testTime)
    database.insertOrUpdateTask(testName, testTimeUpdate)

    # Now check database
    checkPath = os.path.join(temp, "task.db")
    checkDB = sqlite3.connect(checkPath)
    checkTable = database.tableName()
    checkCMD = ("""SELECT id, taskName, taskTime FROM """ + 
                checkTable)
    with checkDB:
        cursor = checkDB.cursor()
        cursor.execute(checkCMD)
        res = cursor.fetchall()
    checkDB.close()

    assert res[0] == expected

def test_getTaskTime(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    testName = "TEST"
    testTime = 10

    name = database.tableName()

    testDB = sqlite3.connect(database.DBNAME)
    addTableCMD = ("""CREATE TABLE """ + name +
                    """ (id INTEGER PRIMARY KEY, 
                        taskName text, taskTime, int)""")

    addTaskCMD = ("""INSERT INTO """ + name +
                    """(taskName, taskTime) VALUES(?, ?)""")
    with testDB:
        cursor = testDB.cursor()
        cursor.execute(addTableCMD)
        cursor.execute(addTaskCMD, (testName, testTime))
    testDB.close()

    res = database.getTaskTime(testName)

    assert res[0] == testTime

def test_taskExists(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    testName = "TEST"
    testTime = 10

    name = database.tableName()

    testDB = sqlite3.connect(database.DBNAME)
    addTableCMD = ("""CREATE TABLE """ + name +
                    """ (id INTEGER PRIMARY KEY, 
                        taskName text, taskTime, int)""")

    addTaskCMD = ("""INSERT INTO """ + name +
                    """(taskName, taskTime) VALUES(?, ?)""")
    with testDB:
        cursor = testDB.cursor()
        cursor.execute(addTableCMD)
        cursor.execute(addTaskCMD, (testName, testTime))
    testDB.close()

    res = database.taskExists(testName)

    assert res

def test_ensureTableExists(tmpdir):

    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = database.tableName()

    database.ensureTableExists(name)

    cmd = "SELECT name FROM sqlite_master WHERE type='table'"

    testDB = sqlite3.connect(database.DBNAME)

    with testDB:
        cursor = testDB.cursor()
        cursor.execute(cmd)
        res = cursor.fetchall()
    testDB.close()


    assert len(res) > 0

def test_getDays(tmpdir):

    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = "DAY_01_01_2000"
    expected = "01/01/2000"
    cmd = ("""CREATE TABLE IF NOT EXISTS """ + name +
            """ (id INTEGER PRIMARY KEY, taskName text, taskTime int)""")

    testDB = sqlite3.connect(database.DBNAME)

    with testDB:
        cursor = testDB.cursor()
        cursor.execute(cmd)
    testDB.close()

    res = database.getDays()

    assert res[0] == expected

def test_getDateTasks(tmpdir):

    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = "DAY_01_01_2000"
    date = datetime.datetime.strptime(name, "DAY_%d_%m_%Y")
    cmd1 = ("""CREATE TABLE IF NOT EXISTS """ + name +
            """ (id INTEGER PRIMARY KEY, taskName text, taskTime int)""")
    cmd2 = ("""INSERT INTO """ + name + 
            """ (taskName, taskTime) VALUES(?, ?)""")
    expectedTask = "TEST_TASK"
    expectedTime = 10
    cmd2Values = (expectedTask, expectedTime)

    testDB = sqlite3.connect(database.DBNAME)

    with testDB:
        cursor = testDB.cursor()
        cursor.execute(cmd1)
        cursor.execute(cmd2, cmd2Values)
    testDB.close()

    expectedObject = database.TaskData(expectedTask,
                                        expectedTime)
    ret = database.getDateTasks(date)
    assert ret[0] == expectedObject

def test_removeDay(tmpdir):

    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = "DAY_01_01_2000"
    date = datetime.datetime.strptime(name, "DAY_%d_%m_%Y")
    cmd1 = ("""CREATE TABLE IF NOT EXISTS """ + name +
            """ (id INTEGER PRIMARY KEY, taskName text, taskTime int)""")
    cmd2 = ("""SELECT name FROM sqlite_master WHERE type='table'""")

    testDB = sqlite3.connect(database.DBNAME)

    with testDB:
        cursor = testDB.cursor()
        cursor.execute(cmd1)

    database.removeDay(date)

    with testDB:
        cursor = testDB.cursor()
        cursor.execute(cmd2)
        ret = cursor.fetchall()
    testDB.close()

    assert len(ret) == 0