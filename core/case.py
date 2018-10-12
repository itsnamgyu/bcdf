# -*- coding: utf-8 -*-

import abc


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


class StdInputTest(TestCase):
    @classmethod
    def from_file(cls, path):
        with open(path, 'w') as f:
            return StdInput(f.read())

    def __init__(self, string):
        self.string = string

    def prepare(self, working_path) -> None:
        return

    def get_stdin(self) -> str:
        return self.string

    def set(self, string: str) -> None:
        self.string = string

    def append(self, string: str) -> None:
        self.string += string

    def clean(self, working_path) -> None:
        return


def main():
    print('nothing to show here!')


if __name__ == '__main__':
    main()
