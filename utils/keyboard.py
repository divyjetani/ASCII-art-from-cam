import os
import sys

IS_WINDOWS = os.name == "nt"

if IS_WINDOWS:
    import msvcrt
else:
    import termios
    import tty
    import select


class Keyboard:
    def __enter__(self):
        if not IS_WINDOWS:
            self.fd = sys.stdin.fileno()
            self.old = termios.tcgetattr(self.fd)
            tty.setcbreak(self.fd)
        return self

    def __exit__(self, *args):
        if not IS_WINDOWS:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)


def get_key():
    if IS_WINDOWS:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            try:
                return key.decode("utf-8").lower()
            except:
                return None
        return None
    else:
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None
