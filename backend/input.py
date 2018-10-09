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
        Return path to file with stdin contents. Will use redirection to
        pass it to the student's program.

        cat get_stdin() | python3 assignment.py
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
    INPUT_TXT = '.bcdf_test_stdin.txt'

    @classmethod
    def from_file(cls, path):
        with open(path, 'w') as f:
            return StdInput(f.read())

    @classmethod
    def from_immediate_file(cls, name=None):
        comment = '\n'
        if name:
            comment += '# Enter input for test case {}\n'.format(name)
        else:
            comment += '# Enter input for test case.\n'
        comment += '# Lines strictly starting with # will be ignored.\n'
        comment += '# Use "\\#" to put # at the start of a line.\n'
            
        # get original string from file
        with tempfile.NamedTemporaryFile('w+', delete=False) as f:
            path = f.name
            f.write(comment)
            f.flush()
            subprocess.call([EDITOR, f.name])
        with open(path) as f:
            original_string = f.read()
        try:
            os.remove(path)
        except OSError:
            pass

        # process comments
        string = ''
        for line in original_string.splitlines():
            if line[0:1] == '#':
                continue
            if line[0:2] == '\\#':
                line = '#' + line[2:]
            string += line + '\n'

        return cls(string)

    def __init__(self, string):
        self.string = string

    def prepare(self, working_path) -> None:
        return

    def get_stdin(self) -> str:
        with open(StdInput.INPUT_TXT, 'w') as f:
            f.write(self.string)
        return StdInput.INPUT_TXT

    def clean(self, working_path) -> None:
        os.remove(StdInput.INPUT_TXT)
        return
