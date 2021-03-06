# TASKLOG

## What is this?

This is a test application written in Python which keeps track of how much time you spend on tasks.

## Setup

### Requirements

This has only been tested on Arch Linux 64bit using Python 3.6.5. It should work on Mac, but will not work on Windows without modifications and extra modules.

* Python 3 [Get it here](https://www.python.org/getit/). Only version 3.6.5 has been tested with this application.
* PIP. You should have it already if you have a recent Python version, see [here](https://pip.pypa.io/en/stable/installing/) if you don't or are not sure

To install the rest of the dependencies run the setup script. It uses `sudo` so feel free to inspect the file before running.

`./setup.sh install`

## Usage

There are four commands

`./tasklog start [TASK_NAME]`\
`./tasklog ls`\
`./tasklog show [DATE]`\
`./tasklog rm [DATE]`

### start

`./tasklog start [TASK_NAME]`

[TASK_NAME] is the name of the task you want to track. It can be any string, within reason. If you want to use spaces in your task name, wrap it in quotes.

A display will appear with a clock that counts up. You can:

* Press ENTER to save the task to file and exit
* Press p to pause the timer and again to restart
* Press q to exit without comitting to file

If you record a task multiple times in one day, the time will be cumulative.

Example:

`./tasklog start emails`\
`./tasklog start coding`\
`./tasklog start procrastination`\
`./tasklog start "Q4 meeting"`

### ls

`./tasklog ls`

Prints out which days you have recorded tasks on.

### show

`./tasklog show [DATE]`

Shows details of what tasks you did on a day, and how long you spent on them. If a task was done multiple times, the time shown will be the total time.

[DATE] is an optional argument of the format `DD/MM/YYYY`, specifying which day you want to show details of. If you omit it, it will show details about todays tasks

Example:

`./tasklog show`\
`./tasklog show 19/07/2018`\
`./tasklog show 01/11/1973`

### rm

`./tasklog rm [DATE]`

This removes from file details about the specified day.

[DATE] is required and is in the format `DD/MM/YYYY`. It specifies which day you want to remove.

Example

`./tasklog rm 19/07/2018`\
`./tasklog rm 01/11/1973`

## Testing

Testing uses pytest. Run `./setup.sh test` to start.

## Troubleshooting

If `./tasklog` does not work you can try `./tasklog.py`. The former is just a symlink to the latter.
