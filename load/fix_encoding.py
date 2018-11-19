import sys

import lib


def main():
    if len(sys.argv) != 1:
        print('Usage: python fix_encoding.py filename')
        return

    filename = sys.argv[1]

    with lib.auto_open(filename) as f:
        string = f.read()

    with open(filename, "w") as f:
        f.write(string)

if __name__ == '__main__':
    main()
