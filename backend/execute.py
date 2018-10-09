import abc
from typing import Tuple


class Runner(object):
    __metaclass__ = abc.ABCMeta

    def __init__():
        pass

    @abc.abstractmethod
    def compile_and_run(program_path, stdin_path) -> Tuple[bool, str, str]:
        '''
        Compile the program, run it, and get output

        Arguments
        - program_path: path of .c, .py etc.
        - stdin_path: path of file with stdin (will passing using pipe)

        Return values
        - 0: whether compilation and run was a success
        - 1: stdout (from program)
        - 2: description
        '''
        return
