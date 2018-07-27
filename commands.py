import display
import database

from time import sleep
import sys
from datetime import datetime

def start(_taskName):

    database.initDirectories()

    lastTime = 0
    delta = 0
    timer = 0
    dateText = "0"

    header = "You have been doing " + _taskName + " for "
    headerText = display.TextElement(header, 0)
    timeText = display.TextElement(dateText, 1)
    break1 = display.TextElement("", 2)
    status = display.TextElement("RECORDING", 3)
    break2 = display.TextElement("", 4)

    instrTextEnter = "Press ENTER to end task and save"
    instrTextP = "Press p to pause task"
    instrTextQ = "Press q to exit without saving task"

    instr1 = display.TextElement(instrTextEnter, 5)
    instr2 = display.TextElement(instrTextP, 6)
    instr3 = display.TextElement(instrTextQ, 7)

    elements = [headerText, timeText, break1, status, break2, instr1, instr2, instr3]
    elements.sort()

    screen = display.initDisplay()

    display.update(screen, elements)

    paused = False

    lastTime = datetime.now()

    while(True):

        delta = datetime.now() - lastTime
        lastTime = datetime.now()
        if not paused:
            timer += delta.total_seconds()
            minutes = int(timer)
            minutesTxt = str(minutes) + " minutes"

        timeText.txt = minutesTxt

        display.update(screen, elements)

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
        elif inp in ('KEY_ENTER', '\n', '\r'):

            taskObj = database.TaskData(_taskName, minutes)
            database.storeTask(taskObj)
            display.end(screen)
            sys.exit(0)

        sleep(0.01)

    display.endCurses(screen)

def ls():

    days = database.getDays()

    for d in days:
        print(d)

def show(dateStr=None):

    print(dateStr)
    if dateStr is None:
        date = datetime.now().date()
    else:
        try:
            date = datetime.strptime(dateStr, "%d/%m/%Y").date()
        except ValueError as err:
            print("Date format must be as follows: DD/MM/YYYY")
            sys.exit(1)

    today = date == datetime.now().date()

    tasks = database.getDateTasks(date)

    elements = []
    prio = 0

    if today:
        headerStart = "Today "
    else:
        headerStart = "On " + date.strftime("%d/%m/%Y") + " "

    header = (headerStart + "you did the following tasks: ")
    headerText = display.TextElement(header, prio)
    prio += 1
    elements.append(headerText)

    break1 = display.TextElement("", prio)
    prio += 1
    elements.append(break1)

    for t in tasks:
        txt = t.name + " for " + str(t.time) + " minutes"
        elements.append(display.TextElement(txt, prio))
        prio += 1

    break2 = display.TextElement("", prio)
    prio += 1
    elements.append(break2)

    instrTextEnter = "Press q or ENTER to exit"
    instr1 = display.TextElement(instrTextEnter, prio)
    elements.append(instr1)

    elements.sort()

    screen = display.initDisplay()

    display.update(screen, elements)

    while(True):

        display.update(screen, elements)

        inp = display.run(screen)

        if inp in ('KEY_ENTER', '\n', '\r', 'q', 'Q'):
            display.end(screen)
            sys.exit(0)

        sleep(0.01)

    display.endCurses(screen)

def rm(dateStr):
    try:
        date = datetime.strptime(dateStr, "%d/%m/%Y").date()
    except ValueError as err:
        print("Date format must be as follows: DD/MM/YYYY")
        sys.exit(1)

    database.removeDay(date)



