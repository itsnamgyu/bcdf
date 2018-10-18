import sys
sys.path.append('..')

import os
import glob
import re
from collections import defaultdict
import shutil


if os.path.exists('source'):
    print('source directory (or file) already exists. moving to source.bak')
    if os.path.exists('source.bak'):
        shutil.rmtree('source.bak')
    os.rename('source', 'source.bak')

os.makedirs('source', exist_ok=True)

while True:
    try:
        n_problems = int(input('how many problems: '))
        break
    except ValueError:
        pass

while True:
    path = input('directory containing source files: ')
    sources = glob.glob('{}/**/*.c'.format(path), recursive=True)
    if not sources:
        print('no files')
    else:
        break

key_re = re.compile('(20[0-9]{6})')

sources.sort()
students = defaultdict(list)

for source in sources:
    match = key_re.search(source)
    students[match.group(1)].append(source)

for key, paths in students.items():
    if len(paths) == n_problems:
        for i, path in enumerate(paths):
            base = os.path.basename(path)
            name, ext = os.path.splitext(base)
            dest = os.path.join('source', '{}_p{}{}'.format(key, i + 1, ext))
            shutil.copy(path, dest)
    else:
        print(key.center(100, '-'))
        for path in paths:
            print(path)
            base = os.path.basename(path)
            dest = os.path.join('source', '{}_{}'.format(key, base))
            shutil.copy(path, dest)

print('done. fix any conflicts before proceeding.')
