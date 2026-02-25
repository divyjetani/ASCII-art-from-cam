import sys

def init_terminal():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def draw(text):
    sys.stdout.write("\033[H")
    sys.stdout.write(text)
    sys.stdout.flush()

def restore_terminal():
    # Clear screen and move cursor to bottom
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
