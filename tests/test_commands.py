"""
test_commands.py

Tests for commands.py
"""

# core
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# project
import commands

def test_get_minutes_seconds():
    # 67 seconds should equal ...
    test_seconds = 67
    # ... 1 minute 7 seconds
    expected = (1, 7)
    result = commands.get_minutes_seconds(test_seconds)

    assert result == expected

def test_make_time_string_sing():

    test_seconds = 67
    expected = "1 minute and 7 seconds"
    result = commands.make_time_string(test_seconds)

    assert result == expected

def test_make_time_string_plural():

    test_seconds = 127
    expected = "2 minutes and 7 seconds"
    result = commands.make_time_string(test_seconds)

    assert result == expected