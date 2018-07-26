#!/usr/bin/env python

# Python Core
import sys

# Third party
import argparse

# Project
import commands

def arguments(inArgs):

    cmd = ('start', 'show', 'ls')

    desc="""A utility for keeping track of how much time
            you have spent on tasks"""
    argParse = argparse.ArgumentParser(description=desc)
    argParse.add_argument('command', choices=cmd)
    argParse.add_argument('subcommand')

    return argParse.parse_args(inArgs)

def main():
    args = arguments(sys.argv[1:])

    if args.command == 'start':

        if not args.subcommand:
            print("The start command requires the name of a task to start")
            sys.exit(1)

        if not isinstance(args.subcommand, str):
            print("The name of the task to start must be a string")
            sys.exit(1)

        commands.start(args.subcommand)

if __name__ == '__main__':
    main()
