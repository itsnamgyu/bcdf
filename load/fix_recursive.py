import sys
import json
import os
import lib
import glob
from tqdm import tqdm


def main():
    if len(sys.argv) != 2:
        print('Usage: python fix_recursive.py path')
        return

    root = sys.argv[1]
    paths = glob.glob(os.path.join(root, "**", "*.txt"), recursive=True)

    incomplete = []
    try:
        for path in tqdm(paths):
            string = lib.auto_read(path)

            if string is None:
                incomplete.append(path)
            else:
                with open(path, "w") as f:
                    f.write(string)
    except Exception as e:
        print(e)
    finally:
        print("Incomplete:")
        print("-" * 80)
        print(json.dumps(incomplete))
        print("-" * 80)

    print(len(incomplete))

if __name__ == '__main__':
    main()
