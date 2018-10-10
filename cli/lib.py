# -*- coding: utf-8 -*-

import os
import tempfile
import subprocess


EDITOR = os.environ.get('EDITOR', 'vim')


def edit_string(string='', title=None) -> str:
    content = string

    if '\n' not in string:
        content += '\n'
    content += '\n'

    if title:
        content += '# {}\n'.format(title)
        content += '#\n'

    content += '\n'.join((
        '# Apply your changes and save the file. Lines strictly starting',
        '# with # will be ignored. If you want to put a # at the start',
        '# of a line, use \\#. Do not use \\# for other #\'s.'
    ))
        
    # get original string from file
    with tempfile.NamedTemporaryFile('w+', delete=False, dir='.') as f:
        path = f.name
        f.write(content)
        f.flush()
        subprocess.call([EDITOR, f.name])
    with open(path) as f:
        original_string = f.read()
    os.remove(path)

    # process comments
    string = ''
    for line in original_string.splitlines():
        if line[0:1] == '#':
            continue
        if line[0:2] == '\\#':
            line = '#' + line[2:]
        string += line + '\n'
    string = string[:-1]  # remove \n

    return string


def main():
    string = edit_string('Hello')
    print(string)
    string = edit_string(string)
    print(string)


if __name__ == '__main__':
    main()
