import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import task
import pytest

def test_arguments_start():
    args = task.arguments(["start", "emails"])
    assert args.command == 'start' and args.subcommand == 'emails'

def test_arguments_none():
    with pytest.raises(SystemExit) as ex:
        args = task.arguments([])
    assert ex.type == SystemExit
    