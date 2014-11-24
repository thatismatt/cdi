#!/usr/bin/env python

# Suggested usage: alias cdi='~/bin/cdi/cdi.py /tmp/cdi.out && cd `cat /tmp/cdi.out`'

import curses
import os
import sys
from datetime import datetime
import collections

INCLUDE_HIDDEN = False

log_file = "/tmp/cdi.log"

HEADER_LINES = 4

def log(*msg):
    with open(log_file, "a") as l:
        l.write("[{}] {}\n".format(datetime.now().isoformat(), " ".join(map(unicode, msg))))

def main(result_file):
    x = []
    curses.wrapper(_start, x.append)
    write_result(result_file, x[0])

def _start(stdscr, set_current_dir):

    current_dir = os.path.abspath(".")
    chs = []

    if screen_height_ok(stdscr):
        exit(-1)

    while True:

        raw_listing = list_dir(current_dir)
        listing = filter_dir(raw_listing, chs)

        if len(listing.dirs) == 1 and len(chs) > 0:
            current_dir = os.path.join(current_dir, listing.dirs[0])
            chs = []
        else:
            display_dir(stdscr, current_dir, listing)
            log("current_dir", current_dir)
            c = stdscr.getch()
            if c == ord("\n"):
                if len(chs) == 0:
                    set_current_dir(current_dir)
                    return
                else:
                    current_dir = os.path.join(current_dir, listing.best_match)
                    chs = []
            elif c == 263: # backspace
                if len(chs) == 0:
                    current_dir = os.path.dirname(current_dir)
                else:
                    chs.pop()
            else:
                chs.append(chr(c))

DirectoryListing = collections.namedtuple("DirectoryListing", [
    "dirs",
    "files",
    "best_match",
])

FileStat = collections.namedtuple("FileStat", [
    "name",
    "is_file",
    "is_dir",
])

def screen_height_ok(stdscr):
    (height, width) = stdscr.getmaxyx()
    return height < HEADER_LINES

def list_dir(current_dir):
    def stat(name):
        full_path = os.path.join(current_dir, name)
        return FileStat(
            name,
            is_file=os.path.isfile(full_path),
            is_dir=os.path.isdir(full_path)
        )

    return map(stat, os.listdir(current_dir))

def filter_dir(in_dirs, chs):
    log("list_dir")
    log(in_dirs)
    prefix = "".join(chs)

    def _is_included(x):
        return (
            x.is_dir and
            (INCLUDE_HIDDEN or x.name[0] != ".") and
            dirs_scores[x.name] > 0
        )

    def _is_file(x):
        return (
            x.is_file and
            (INCLUDE_HIDDEN or x.name[0] != ".")
        )

    dirs_scores = collections.OrderedDict(
        (in_dir.name, score_match(chs, in_dir.name))
        for in_dir in sorted(in_dirs)
        if in_dir.is_dir
    )
    dirs = sorted(filter(_is_included, in_dirs))
    files = sorted(filter(_is_file, in_dirs))
    log(chs)
    log(dirs)

    def extract_names(stats):
        return [stat.name for stat in stats]

    if chs == []:
        best_match = None
    else:
        best_match = max(dirs_scores.keys(), key=dirs_scores.get)

    return DirectoryListing(extract_names(dirs), extract_names(files), best_match)

def score_match(chs, name):
    score = 1
    index = -1
    for ch in chs:
        index = name.find(ch, index + 1)
        if index == -1:
            return 0
        else:
            score += 1000000 - index
            if index == 0 or name[index - 1] in "-_ .":
                score += 2000000
    return score

def display_dir(stdscr, current_dir, listing):
    log("display_dirs")
    stdscr.clear()
    (height, width) = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.addstr(current_dir + "\n", curses.color_pair(1))
    dirs = listing.dirs[:height - HEADER_LINES]
    files = listing.files[:height - len(dirs) - HEADER_LINES]
    for name in dirs:
        if name == listing.best_match:
            stdscr.addstr(name + "\n", curses.color_pair(2))
        else:
            stdscr.addstr(name + "\n")
    stdscr.addstr("\nFiles\n", curses.color_pair(1))
    for name in files:
        stdscr.addstr(name + "\n")

def write_result(filename, result):
    with open(filename, "w") as f:
        f.write(result)

if __name__ == "__main__":
    main(sys.argv[1])
