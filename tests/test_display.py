"""
test_display.py

tests for display.py
"""
# core
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import mock
import curses

# project
import display

@mock.patch('display.curses')
def test_init_display(mock_curses):

    """
    curses.cbreak() requires terminal, it
    will fail if run in the background, like when
    you run pytest
    """
    mock_curses.cbreak.return_value = None

    scr = display.init_display()
    assert not type(scr) is None

@mock.patch('display.curses')
def test_end(mock_curses):
    mock_curses.cbreak.return_value = None
    mock_curses.nocbreak.return_value = None

    scr = display.init_display()
    display.end(scr)

    assert mock_curses.isendwin()

def test_title():
    screen = curses.initscr()
    display.title(screen)
    assert screen.is_wintouched()

def test_update():
    screen = curses.initscr()
    elements = [display.TextElement("test", 0)]
    display.update(screen, elements)
    assert screen.is_wintouched()




