import display
from time import sleep
import sys
from datetime import datetime

def start(_taskName):

    elements = {}

    header = "You have been doing " + _taskName + " for "

    elements['header'] = display.TextElement(header, 0, 3)

    screen = display.init()

    display.update(screen, elements)

    startTime = datetime.now()
    delta = datetime.now() - startTime

    dateText = str(delta)
    elements['time'] = display.TextElement(dateText, 0, 4)

    while(True):

        delta = datetime.now() - startTime
        minutes = str(int(delta.total_seconds() / 60))
        minutes = minutes + " minutes"

        elements['time'].txt = minutes

        display.update(screen, elements)

        inp = display.run(screen)

        if inp in ('q', 'Q'):
            display.end(screen)
            sys.exit(0)

        sleep(0.01)

    display.endCurses(screen)

