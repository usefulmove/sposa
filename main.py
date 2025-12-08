import sys


def sposa():
    file: str = sys.argv[1]

    print(f"{file=}")

    with open(file, 'r') as file:
        content = file.read()

    words = content.split()

    for word in words:
        print(word)

    print("hello sposa.")


if __name__ == "__main__":
    sposa()
