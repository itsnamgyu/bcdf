# -*- coding: utf-8 -*-

import abc
import os
import sys
import tempfile
import subprocess

import manual_io as mio


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

    @classmethod
    def from_immediate_file(cls, title=None):
        if title:
            string = mio.edit_string(title='Testcase Input [{}]'.format(title))
        else:
            string = mio.edit_string(title='Testcase Input')
        return cls(string)

    def __init__(self, string):
        self.string = string

    def prepare(self, working_path) -> None:
        return

    def get_stdin(self) -> str:
        return self.string

    def edit(self) -> None:
        self.string = mio.edit_string(title='Edit String', string=self.string)

    def set(string: str) -> None:
        self.string = string

    def append(string: str) -> None:
        self.string += string

    def clean(self, working_path) -> None:
        return


def main():
    print(StdInput.from_immediate_file().string)


if __name__ == '__main__':
    main()
