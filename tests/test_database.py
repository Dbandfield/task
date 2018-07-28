"""
test_database.py

Tests for database.py
"""

# core
import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3

# project
import database

def test_init_directories(tmpdir):

    temp = tmpdir.mkdir("tmp")
    new_dir = os.path.join(temp, 'new')
    database.DATA_DIR = new_dir
    database.init_directories()
    assert os.path.isdir(new_dir)

def test_connect(tmpdir):

    temp = tmpdir.mkdir("tmp")
    new_dir = os.path.join(temp, 'new')
    database.DATA_DIR = new_dir
    db = database.connect()
    assert type(db) is sqlite3.Connection

def test_store_task(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    test_data = database.TaskData('TEST', 10)
    expected = (1, 'TEST', 10)

    database.store_task(test_data)

    # Now check database
    check_path = os.path.join(temp, "task.db")
    check_db = sqlite3.connect(check_path)
    check_table = database.table_name()
    check_cmd = ("""SELECT id, task_name, task_time FROM """ +
                 check_table)
    with check_db:
        cursor = check_db.cursor()
        cursor.execute(check_cmd)
        res = cursor.fetchall()
    check_db.close()

    assert res[0] == expected

def test_insert_or_update_task_insert(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    test_name = "TEST"
    test_time = 10
    expected = (1, 'TEST', 10)

    database.insert_or_update_task(test_name, test_time)

    # Now check database
    check_path = os.path.join(temp, "task.db")
    check_db = sqlite3.connect(check_path)
    check_table = database.table_name()
    check_cmd = ("""SELECT id, task_name, task_time FROM """ +
                 check_table)
    with check_db:
        cursor = check_db.cursor()
        cursor.execute(check_cmd)
        res = cursor.fetchall()
    check_db.close()

    assert res[0] == expected

def test_insert_or_update_task_update(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    test_name = "TEST"
    test_time = 10
    test_time_update = 11
    expected = (1, 'TEST', 11)

    database.insert_or_update_task(test_name, test_time)
    database.insert_or_update_task(test_name, test_time_update)

    # Now check database
    check_path = os.path.join(temp, "task.db")
    check_db = sqlite3.connect(check_path)
    check_table = database.table_name()
    check_cmd = ("""SELECT id, task_name, task_time FROM """ +
                 check_table)
    with check_db:
        cursor = check_db.cursor()
        cursor.execute(check_cmd)
        res = cursor.fetchall()
    check_db.close()

    assert res[0] == expected

def test_get_task_time(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    test_name = "TEST"
    test_time = 10

    name = database.table_name()

    test_db = sqlite3.connect(database.DBNAME)
    add_table_cmd = ("""CREATE TABLE """ + name +
                     """ (id INTEGER PRIMARY KEY,
                     task_name text, task_time, int)""")

    add_task_cmd = ("""INSERT INTO """ + name +
                    """(task_name, task_time) VALUES(?, ?)""")
    with test_db:
        cursor = test_db.cursor()
        cursor.execute(add_table_cmd)
        cursor.execute(add_task_cmd, (test_name, test_time))
    test_db.close()

    res = database.get_task_time(test_name)

    assert res[0] == test_time

def test_task_exists(tmpdir):

    temp = tmpdir.mkdir("tmp")

    database.DBNAME = os.path.join(temp, 'task.db')

    test_name = "TEST"
    test_time = 10

    name = database.table_name()

    test_db = sqlite3.connect(database.DBNAME)
    add_table_cmd = ("""CREATE TABLE """ + name +
                     """ (id INTEGER PRIMARY KEY,
                     task_name text, task_time, int)""")

    add_task_cmd = ("""INSERT INTO """ + name +
                    """(task_name, task_time) VALUES(?, ?)""")
    with test_db:
        cursor = test_db.cursor()
        cursor.execute(add_table_cmd)
        cursor.execute(add_task_cmd, (test_name, test_time))
    test_db.close()

    res = database.task_exists(test_name)

    assert res

def test_table_exists_true(tmpdir):
    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = "DAY_01_01_2000"
    add_table_cmd = ("""CREATE TABLE """ + name +
                     """ (id INTEGER PRIMARY KEY,
                     task_name text, task_time, int)""")

    test_db = sqlite3.connect(database.DBNAME)
    with test_db:
        cursor = test_db.cursor()
        cursor.execute(add_table_cmd)
    test_db.close()

    assert database.table_exists(name)


def test_table_exists_false(tmpdir):
    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = database.table_name()

    test_db = sqlite3.connect(database.DBNAME)
    test_db.close()

    assert not database.table_exists(name)

def test_ensure_table_exists(tmpdir):

    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = database.table_name()

    database.ensure_table_exists(name)

    cmd = "SELECT name FROM sqlite_master WHERE type='table'"

    test_db = sqlite3.connect(database.DBNAME)

    with test_db:
        cursor = test_db.cursor()
        cursor.execute(cmd)
        res = cursor.fetchall()
    test_db.close()


    assert len(res) > 0

def test_get_days(tmpdir):

    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = "DAY_01_01_2000"
    expected = "01/01/2000"
    cmd = ("""CREATE TABLE IF NOT EXISTS """ + name +
           """ (id INTEGER PRIMARY KEY, task_name text, task_time int)""")

    test_db = sqlite3.connect(database.DBNAME)

    with test_db:
        cursor = test_db.cursor()
        cursor.execute(cmd)
    test_db.close()

    res = database.get_days()

    assert res[0] == expected

def test_get_date_tasks(tmpdir):

    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = "DAY_01_01_2000"
    date = datetime.datetime.strptime(name, "DAY_%d_%m_%Y")
    cmd1 = ("""CREATE TABLE IF NOT EXISTS """ + name +
            """ (id INTEGER PRIMARY KEY, task_name text, task_time int)""")
    cmd2 = ("""INSERT INTO """ + name +
            """ (task_name, task_time) VALUES(?, ?)""")
    expected_task = "TEST_TASK"
    expected_time = 10
    cmd2_values = (expected_task, expected_time)

    test_db = sqlite3.connect(database.DBNAME)

    with test_db:
        cursor = test_db.cursor()
        cursor.execute(cmd1)
        cursor.execute(cmd2, cmd2_values)
    test_db.close()

    expected_object = database.TaskData(expected_task,
                                        expected_time)
    ret = database.get_date_tasks(date)
    assert ret[0] == expected_object

def test_remove_day(tmpdir):

    temp = tmpdir.mkdir("tmp")
    database.DBNAME = os.path.join(temp, 'task.db')
    name = "DAY_01_01_2000"
    date = datetime.datetime.strptime(name, "DAY_%d_%m_%Y")
    cmd1 = ("""CREATE TABLE IF NOT EXISTS """ + name +
            """ (id INTEGER PRIMARY KEY, task_name text, task_time int)""")
    cmd2 = ("""SELECT name FROM sqlite_master WHERE type='table'""")

    test_db = sqlite3.connect(database.DBNAME)

    with test_db:
        cursor = test_db.cursor()
        cursor.execute(cmd1)

    database.remove_day(date)

    with test_db:
        cursor = test_db.cursor()
        cursor.execute(cmd2)
        ret = cursor.fetchall()
    test_db.close()

    assert len(ret) == 0

def test_sanitise_table_name_good():
    good_name = "DAY_01_01_2000"
    test_name = database.sanitise_table_name(good_name)
    assert good_name == test_name

def test_sanitise_table_name_bad():
    bad_name = "(><?;:'~#][}{)(=+-!\"£$%^&*DAY_01_01_2000"
    expected = "DAY_01_01_2000"
    test_name = database.sanitise_table_name(bad_name)
    assert test_name == expected