"""
display.py

Contains functions for displaying text via curses

initDispay() -- sets up curses

end(scr) -- gracefully stops curses

title(scr) -- Add a title to the window

update(scr, elements) -- Add text to the window

run(scr) -- Get user input

class TextElement -- A simple class that holds information
on a piece of text on the screen
"""

# core
import curses

def init_display():
    """
    Intialise curses.

    Returns a curses window object
    """
    scr = curses.initscr()
    # Do not echo user input
    curses.noecho()
    # makes all key presses available to the program
    curses.cbreak()
    scr.keypad(True)

    # Makes getkey() non-blocking
    scr.nodelay(True)

    # Add a title
    title(scr)
    return scr

def end(scr):
    """
    Provide a curses Window object.

    Ends curses gracefully
    """
    curses.nocbreak()
    scr.keypad(False)
    curses.echo()
    curses.endwin()

def title(scr):
    """
    Provide a curses Window object

    Add a title to the window
    """

    title_txt = "TASKLOG"

    scr.addstr(0, 0, title_txt)

def update(scr, elements):
    """
    Provide a curses Window object and a list
    of TextElements (see class below)

    Adds the elements to the window
    """

    # clear the window
    scr.erase()

    # add the title
    title(scr)

    # add the elements
    x = 0
    y = 2

    for el in elements:
        scr.addstr(y, x, el.txt)
        y += 1

def run(scr):
    """
    Provide a curses Window object

    Checks for user input

    Returns a string corresponding to the key press, or
    None if no key was pressed.

    This either corresponds directly to the key pressed
    or is a special curses string for non-printable characters
    (refer to curses documentation for these strings)
    """

    c = None
    try:
        c = scr.getkey()
    except curses.error as err:
        """
        ignore, because this just indicates
        no key was pressed
        """

    return c

class TextElement:
    """
    A simple class, representing an element of text
    in the window.

    It has two properties:
    txt -- the text string
    priority -- an integer. The lower the number, the
    higher up the page the text is.
    """

    def __init__(self, txt, priority):
        """
        Provide the text content as a string and
        the priority of the element as an integer
        """

        if not isinstance(txt, str):
            raise TypeError("txt should be a string")
        if not isinstance(priority, int):
            raise TypeError("priority should be an integer")
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
