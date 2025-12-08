#!/usr/bin/env python
import sys
from time import sleep
# from rich import Console


def sposa():
    filename: str = sys.argv[1]

    with open(filename, "r") as file:
        content = file.read()

    words = content.split()

    # hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        sys.stdout.write("\r\033[2K" + f"  {words[0]}  ")
        sys.stdout.flush()

        sleep(1.0)


        for word in words:
            # clear line properly
            sys.stdout.write("\r\033[2K" + f"  {word}  ")
            sys.stdout.flush()

            sleep(0.318)

            # increase delay for punctuation
            if word and word[-1] in ".,:!?;":
                sleep(0.280)

    finally:
        # show cursor again
        sys.stdout.write("\033[?25h")
        sys.stdout.write("\n")
        sys.stdout.flush()


    sleep(1.0)


if __name__ == "__main__":
    sposa()
