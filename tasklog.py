#!/usr/bin/env python

import os
# auto-run virtualenv
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
activate = os.path.join(THIS_DIR, 'venv/bin/activate_this.py')
exec(open(activate).read())

# Python Core
import sys

# Third party
import argparse

# Project
import commands

def arguments(inArgs):

    desc="""A utility for keeping track of how much time
            you have spent on tasks"""
    argParse = argparse.ArgumentParser(description=desc)

    subparsers = argParse.add_subparsers(dest='command')
    subparsers.required = True

    startParser = subparsers.add_parser('start')
    startParser.add_argument('task')
    startParser.set_defaults(func=start)

    lsParser = subparsers.add_parser('ls')
    lsParser.set_defaults(func=ls)

    showParser = subparsers.add_parser('show')
    showParser.add_argument('date', nargs='?', const='')
    showParser.set_defaults(func=show)

    rmParser = subparsers.add_parser('rm')
    rmParser.add_argument('date')
    rmParser.set_defaults(func=rm)

    return argParse.parse_args(inArgs)

def main():
    args = arguments(sys.argv[1:])
    args.func(args)

def start(a):
    commands.start(a.task)

def ls(a):
    commands.ls()

def show(a):
    if a.date == '':
        d = None
    else:
        d = a.date
    commands.show(d)

def rm(a):
    commands.rm(a.date)

if __name__ == '__main__':
    main()
