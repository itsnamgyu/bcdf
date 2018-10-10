# -*- coding: utf-8 -*-

import abc
import os
import sys
import tempfile
import subprocess


EDITOR = os.environ.get('EDITOR','vim')


class TestCase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def prepare(self, working_dir) -> None:
        '''
        Prepare environment for the specific test case, such as
        files for file IO.
        '''
        return

    @abc.abstractmethod
    def get_stdin(self) -> str:
        '''
        Return stdin contents to be passed to the student program.
        '''
        return

    @abc.abstractmethod
    def clean(self, working_dir) -> None:
        '''
        Clean up environment after calling the 'prepare' method above.
        '''
        return


def get_y_or_n(verbose=1) -> bool:
    while True:
        if verbose:
            string = input('(y/n) ')
        else:
            string = input()
        if string == 'y':
            return True
        elif string == 'n':
            return False


class StdInput(TestCase):
    INPUT_TXT = '.bcdf_stdin.txt'

    @classmethod
    def from_file(cls, path):
        with open(path, 'w') as f:
            return StdInput(f.read())

    @staticmethod
    def edit_string(title=None, string='') -> str:
        content = string

        if '\n' not in string:
            content += '\n'
        
        if title:
            content += '# {}\n'.format(title)
            content += '#\n'

        content += '# Enter the string and save/close the file. Lines strictly starting with #\n'
        content += '# will be ignored. If you want to put a # at the start of a line, use \\#.\n'
        content += '# Do not use \\# for other #\'s\n'
            
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

        return string

    @classmethod
    def from_immediate_file(cls, title=None):
        if title:
            string = StdInput.edit_string(title='Input For Testcase [{}]'.format(title))
        else:
            string = StdInput.edit_string(title='Input For Testcase')
        return cls(string)

    def __init__(self, string):
        self.string = string

    def prepare(self, working_path) -> None:
        return

    def edit(self) -> None:
        self.string = StdInput.edit_string(title='Edit String', string=self.string)

    def get_stdin(self) -> str:
        return self.string

    def clean(self, working_path) -> None:
        return

# temp test
ho = StdInput.from_immediate_file()
print(ho.get_stdin())
ho.edit()
print(ho.get_stdin())
