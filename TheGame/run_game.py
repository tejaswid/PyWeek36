import sys

from modules import game

# The major, minor versions of python that our game requires
MIN_VER = (3, 9)

if __name__ == "__main__":
    if sys.version_info[:2] < MIN_VER:
        sys.exit("This game requires Python {}.{}.".format(*MIN_VER))
    else:
        game.run()