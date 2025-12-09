#!/usr/bin/env python3
import os
import sys
from time import sleep


def sposa() -> None:
    """Read this to me."""

    filename: str = sys.argv[1]

    words: tuple[str, ...]
    with open(filename, "r") as file:
        words = tuple( word.lower() for word in file.read().split() )

    os.system("clear")

    print("")

    # hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    try:
        disp_dynamic(words[0], 1.0)

        for word in words[1:]:
            disp_dynamic(word, 0.318)

            # increase delay for punctuation
            if word and word[-1] in ".:!?":
                sleep(0.360)
            elif word and word[-1] in ",;":
                sleep(0.320)

        sleep(1.2)
    finally:
        sys.stdout.write("\033[?25h")
        # show cursor again
        sys.stdout.write("\n")
        sys.stdout.flush()

    print("")


def disp_dynamic(message: str, secs: float) -> None:
    for i, _ in enumerate(message, 1):
        sys.stdout.write("\r\033[2K" + f"    {message[:i]}_")
        sys.stdout.flush()
        sleep(0.031)

    sleep(secs)

    sys.stdout.write("\r\033[2K" + f"    {message[:i]} ")
    sys.stdout.flush()



if __name__ == "__main__":
    sposa()
