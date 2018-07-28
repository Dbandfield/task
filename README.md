# TASKLOG

## What is this?

This is a test application written in Python which keeps track of how much time you spend on tasks.

## Requirements

This has only been tested on Arch Linux 64bit. It should work on Mac, but probably will not work on Windows (because of the bash scripts and the curses library).

* Python 3 [Get it here](https://www.python.org/getit/)
* virtualenv. This allows packages to be installed local to a project. Run `./util.sh install_global_dependencies` to install it. This uses `sudo`, so feel free to take a look at the file before running it.

All other dependencies are local to the project and can be installed by running `./util.sh install_local_dependencies`. For reference these are:

* atomicwrites==1.1.5
* attrs==18.1.0
* mock==2.0.0
* more-itertools==4.2.0
* pbr==4.2.0
* pluggy==0.6.0
* py==1.5.4
* pytest==3.6.3
* six==1.11.0

### virtualenv setup

If you did not install virtualenv from `util.sh` you will also need to set it up by running `./util.sh setup_virtualenv`

## Usage

There are four commands

### start

`./tasklog.py start [TASK_NAME]`

[TASK_NAME] is the name of the task you want to track. It can be any string, within reason.

A display will appear with a clock that counts up. You can:

* Press ENTER to save the task to file and exit
* Press p to pause the timer and again to restart
* Press q to exit without comitting to file

If you record a task multiple times in one day, the time will be cumulative.

#### Example

`./tasklog.py start emails`\
`./tasklog.py start coding`\
`./tasklog.py start procrastination`

### ls

`./tasklog.py ls`

Prints out which days you have recorded tasks on.

### show

`./tasklog.py show [DATE]`

Shows details of what tasks you did on a day, and how long you spent on them. If a task was done multiple times, the time shown will be the total time.

[DATE] is an optional argument of the format `DD/MM/YYYY`, specifying which day you want to show details of. If you omit it, it will show details about todays tasks

#### Example

`./tasklog show`\
`./tasklog show 19/07/2018`\
`./tasklog show 01/11/1973`

### rm

`./tasklog.py rm [DATE]`

This removes from file details about the specified day.

[DATE] is required and is in the format `DD/MM/YYYY`. It specifies which day you want to remove.

#### Example

`./tasklog rm 19/07/2018`\
`./tasklog rm 01/11/1973`

## Testing

Testing uses pytest. Run `./util.sh test` to start.
