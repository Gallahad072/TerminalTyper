import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Type Test")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        color = curses.color_pair(1) if char == target[i] else curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def get_target():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip("\n")


def wpm_test(stdscr):
    start_time = time.time()
    target = get_target()
    current_text = []
    wpm = 0
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if current_text == []:
            start_time = time.time()

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(
            3,
            0,
            "You Did It! Press any key to continue or press Esc to quit.",
            curses.color_pair(3),
        )
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)
