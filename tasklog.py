#!/usr/bin/env python
"""
tasklog

The entry script. It handles arguments, and then
calls the appropriate function from commands.py

arguments(in_args) -- setup arguments
main() -- entry point
start(a) -- handle start command
ls(a) -- handle ls command
show(a) -- handle show command
rm(a) -- handle rm command
"""

import os
# auto-run virtualenv
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ACTIVATE = os.path.join(THIS_DIR, 'venv/bin/activate_this.py')
exec(open(ACTIVATE).read())

# Python Core
import sys

# Third party
import argparse

# Project
import commands


def arguments(in_args):
    """
    Set up argparse and return parsed arguments

    in_args -- a list of string arguments to parse

    returns a Namespace object with the arguments
    """

    desc = """A utility for keeping track of how much time
            you have spent on tasks"""
    arg_parse = argparse.ArgumentParser(description=desc)

    # subparses so that each command can have its
    # own sub commands
    subparsers = arg_parse.add_subparsers(dest='command')
    subparsers.required = True

    # For the start command
    start_parser = subparsers.add_parser('start')
    start_parser.add_argument('task')
    start_parser.set_defaults(func=start)

    # For the ls command
    ls_parser = subparsers.add_parser('ls')
    ls_parser.set_defaults(func=ls)

    # For the show command
    show_parser = subparsers.add_parser('show')
    show_parser.add_argument('date', nargs='?', const='')
    show_parser.set_defaults(func=show)

    # For the rm command
    rm_parser = subparsers.add_parser('rm')
    rm_parser.add_argument('date')
    rm_parser.set_defaults(func=rm)

    return arg_parse.parse_args(in_args)

def main():
    """ Entry point for the script """

    args = arguments(sys.argv[1:])
    # Which function runs is determined by arguments
    args.func(args)

def start(args):
    """
    provide a argparse namespace object.
    Calls the start command
    """
    commands.start(args.task)

def ls(args):
    """
    provide a argparse namespace object.
    Calls the ls command
    """
    commands.ls()

def show(args):
    """
    provide a argparse namespace object.
    Calls the show command
    """

    # If no date supplied, set to None
    if args.date == '':
        d = None
    else:
        d = args.date
    commands.show(d)

def rm(args):
    """
    provide a argparse namespace object.
    Calls the rm command
    """

    commands.rm(args.date)

if __name__ == '__main__':
    main()
