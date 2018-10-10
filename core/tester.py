# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import os
import abc
import subprocess
from typing import Tuple, Dict, List

from core import case
from core import lib


class Tester(object):
    def __init__(self, interpreter=None):
        '''
        Arguments
        - interpreter: python3 in 'python3 foo.py', java in 'java bar.java' etc.
          for more complex situations like python w/ custom environments,
          subclass Testor and override run_single
        '''

        self.interpreter = interpreter

    def run_single(self,
                    executable: str,
                    test : case.TestCase,
                    timeout: int = 2) -> dict:
        '''
        Test executable with single test case and get results

        Override this to support custom execution

        Returns Keys
        - success: bool (required)
        - stdin: string (required)
        - stdout: string (required)
        - stderr: string (required)
        '''
        test.prepare(os.path.dirname(executable))
        stdin = test.get_stdin()
        args = [executable]

        if self.interpreter:
            args.prepend(self.interpreter)
        exec_res = lib.execute([executable], stdin=stdin, timeout=timeout)
        
        res = dict(
            stdin=stdin,
            stdout=exec_res['stdout'],
            stderr=exec_res['stderr']
        )

        res['success'] = (exec_res['returncode'] == 0)

        return res


    def run(self, executable: str, tests: List[case.TestCase], **kwargs) -> List[dict]:
        '''
        Test executable with multiple test cases and return result

        Return
        - list of dictionaries returned by test_single
        '''
        res = list()
        for test in tests:
            res.append(run_single(executable, test, **kwargs))
        return res


def main():
    import compiler as comp
    with comp.CCompiler() as c:
        res = c.compile('example.c')
        for key, value in res.items():
            print(key.center(80, '-'))
            print(value)

        test = case.StdInputTest('hello\n')
        res = Tester().run_single(res['executable'], test)
        for key, value in res.items():
            print(key.center(80, '-'))
            print(value)
    

if __name__ == '__main__':
    main()
