#!/usr/bin/env python

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
    # argParse.add_argument('command', choices=cmd)

    subparsers = argParse.add_subparsers()

    startParser = subparsers.add_parser('start')
    startParser.add_argument('task')
    startParser.set_defaults(func=start)

    lsParser = subparsers.add_parser('ls')
    lsParser.set_defaults(func=ls)

    showParser = subparsers.add_parser('show')
    showParser.add_argument('date', nargs='?', const='')
    showParser.set_defaults(func=show)

    return argParse.parse_args(inArgs)

def main():
    args = arguments(sys.argv[1:])
    args.func(args)

def start(a):
    print("start")
    commands.start(a.task)

def ls(a):
    commands.ls()

def show(a):
    print(a.date)
    if a.date == '':
        d = None
    else:
        d = a.date
    commands.show(d)

if __name__ == '__main__':
    main()
