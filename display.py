import curses

def initDisplay():
    scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    scr.keypad(True)
    scr.nodelay(True)

    title(scr)
    return scr

def end(scr):
    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.endwin()

def title(scr):

    title = "Task Tracker"

    scr.addstr(0, 0, title)

def update(scr, elements):
    scr.erase()
    title(scr)

    x = 0
    y = 2
    
    for el in elements:
        scr.addstr(y, x, el.txt)
        y += 1

def run(scr):

    c = None
    try:
        c = scr.getkey()
    except curses.error as err:
        """ ignore """

    return c

class TextElement:

    def __init__(self, txt, priority):
        self.txt = txt
        self.priority = priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __lt__(self, other):
        return self.priority < other.priority 

    def __ge__(self, other):
        return self.priority >= other.priority

    def __le__(self, other):
        return self.priority <= other.priority 
