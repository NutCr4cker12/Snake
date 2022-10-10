import curses

def create_screen():
    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    screen.keypad(True)
    return screen

def close(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()