import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import tasklog
import pytest

def test_arguments_start():
    args = tasklog.arguments(["start", "emails"])
    assert args.command == 'start' and args.task == 'emails'

def test_arguments_none():
    with pytest.raises(SystemExit) as ex:
        args = tasklog.arguments([])
    assert ex.type == SystemExit
    