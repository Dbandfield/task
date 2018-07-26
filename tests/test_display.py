import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import display
import pytest
import mock
import curses

@mock.patch('display.curses')
def test_initDisplay(mockCurses):

    """
    curses.cbreak() requires terminal, it 
    will fail if run in the background, like when
    you run pytest
    """
    mockCurses.cbreak.return_value = None

    scr = display.initDisplay()
    assert not type(scr) is None

@mock.patch('display.curses')
def test_end(mockCurses):
    mockCurses.cbreak.return_value = None
    mockCurses.nocbreak.return_value = None

    scr = display.initDisplay()
    display.end(scr)

    assert mockCurses.isendwin()

def test_title():
    screen = curses.initscr()
    display.title(screen)
    assert screen.is_wintouched()

def test_update():
    screen = curses.initscr()
    elements = [display.TextElement("test", 0)]
    display.update(screen, elements)
    assert screen.is_wintouched()




