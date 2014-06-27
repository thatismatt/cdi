#!/usr/bin/env python

import curses
import os
import sys
from datetime import datetime

INCLUDE_HIDDEN = False

log_file = "/tmp/cdi.log"

def log(*msg):
    with open(log_file, "a") as l:
        l.write("[{}] {}\n".format(datetime.now().isoformat(), " ".join(map(unicode, msg))))

def main(result_file):
    x = []
    curses.wrapper(_start, x.append)
    write_result(result_file, x[0])

def _start(stdscr, set_current_dir):

    current_dir = "."
    chs = []

    while True:
        dirs = list_dirs(current_dir, os.listdir(current_dir), chs)

        if len(dirs) == 1 and len(chs) > 0:
            current_dir = os.path.join(current_dir, dirs[0])
            chs = []
        elif len(dirs) == 0 and len(chs) == 0:
            log("current_dir", current_dir)
            set_current_dir(current_dir)
            return
        else:
            display_dirs(stdscr, current_dir, dirs, chs)

            log("current_dir", current_dir)

            c = stdscr.getch()
            if c == ord("\n"):
                set_current_dir(current_dir)
                return
            elif c == 263: # backspace
                if len(chs) == 0:
                    # TODO: jump up a dir
                    pass
                else:
                    chs.pop()
            else:
                chs.append(chr(c))

def list_dirs(current_dir, in_dirs, chs):
    log("list_dirs")
    log(in_dirs)
    prefix = "".join(chs)
    def _is_included(d):
        return (
            os.path.isdir(os.path.join(current_dir, d)) and
            (INCLUDE_HIDDEN or d[0] != ".") and
            d.startswith(prefix)
        )

    dirs = sorted(filter(_is_included, in_dirs))
    log(chs)
    log(dirs)
    return dirs

def display_dirs(stdscr, current_dir, dirs, chs):
    log("display_dirs")
    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    current_dir_absolute = os.path.abspath(current_dir)
    stdscr.addstr(current_dir_absolute + "\n", curses.color_pair(1) | curses.A_REVERSE)
    for name in dirs:
        stdscr.addstr(name + "\n")

def write_result(filename, result):
    with open(filename, "w") as f:
        f.write(result)

if __name__ == "__main__":
    main(sys.argv[1])
