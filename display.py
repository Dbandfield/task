import curses

def init():
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

    scr.addstr(1, 0, title)

def update(scr, elements):
    scr.erase()
    title(scr)

    for k, v in elements.items():
        scr.addstr(v.y, v.x, v.txt)

def run(scr):

    c = None
    try:
        c = scr.getkey()
    except curses.error as err:
        """ ignore """

    return c

class TextElement:

    def __init__(self, txt, x, y):
        self.txt = txt
        self.x = x
        self.y = y

    
