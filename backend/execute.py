import os
import abc
import subprocess
from typing import Tuple, Dict


class Executor(object):
    __metaclass__ = abc.ABCMeta

    def __init__():
        pass


    @staticmethod
    def execute(args, stdin='', timeout=1) -> dict:
        '''
        Pass stdin input to executable w/ args and get return code, stdout, stderr string
        '''
        with subprocess.Popen(args,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as p:
            try:
                stdout, stderr = p.communicate(input=stdin.encode(),
                                               timeout=timeout)
            except subprocess.TimeoutExpired as e:
                p.kill()

            return dict(
                returncode=p.returncode,
                stdout=stdout.decode(),
                stderr=stderr.decode())


    @abc.abstractmethod
    def compile_and_execute(self, source_path, stdin_string) -> dict:
        '''
        Compile the program, execute it, and get output

        Arguments
        - source_path: path of .c, .py etc.
        - stdin_string: the contents of stdin to pass to program

        Return values
        - dictionary containing at least keys 'stdout': str, 'success': bool, 'source': str of path
          make sure the keys are in snake-case
        '''
        return


class CExecutor(Executor):
    OUTFILE = os.path.abspath('.bcdf_test_c_program.out')

    def __init__(self, std='gnu11'):
        self.std = std

    def compile_and_execute(self, c_path, stdin_string) -> dict:
        c_path = os.path.abspath(c_path)
        res = dict()

        res['source'] = c_path

        # compilation
        compile_res = Executor.execute(['gcc', '-std=' + self.std, '-o', CExecutor.OUTFILE, c_path])
        if compile_res['returncode'] == 0:
            exec_res = Executor.execute(CExecutor.OUTFILE, stdin_string)
            try:
                os.remove(OUTFILE)
            except OSError:
                pass
            res['stdout'] = exec_res['stdout']
            if exec_res['stderr']:
                res['stderr'] = exec_res['stderr']
            return res
        else:
            res['compile_error'] = compile_res['stderr']
            res['stdout'] = ''
            res['success'] = False
            return res

# temp test
for key, val in CExecutor().compile_and_execute('ho.c', 'Hello World!').items():
    print(key.center(80, '-'))
    print(val)
