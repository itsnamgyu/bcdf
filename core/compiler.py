# -*- coding: utf-8 -*-

import sys
sys.path.append('..')

import os
import abc
import tempfile

from core import lib


class Compiler(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.dirty = False

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> bool:
        self.clean()
        return False

    def compile(self, source_path):
        if self.dirty:
            self.clean()
        res = self._compile(source_path)
        self.dirty = True
        
        return res

    def clean(self) -> None:
        if self.dirty:
            self._clean()
        self.dirty = False

    @abc.abstractmethod
    def _compile(self, source_path) -> dict:
        '''
        Compile the program and return results

        Arguments
        - source_path: path of .c, .py etc.

        Return Keys
        - success: bool (required)
        - executable: path string (required)
        - compile_warnings: string (optional)
        - etc.
        '''
        return

    @abc.abstractmethod
    def _clean(self) -> None:
        '''
        Clean up executable files, intermediate files etc.
        '''


class CCompiler(Compiler):
    def __init__(self, std='gnu11'):
        Compiler.__init__(self)
        self.std = std
        self.outfile = None

    def _compile(self, c_path) -> dict:
        c_path = os.path.abspath(c_path)
        res = dict()

        with tempfile.NamedTemporaryFile(dir='.') as f:
            self.outfile = f.name
        res['executable'] = self.outfile

        compile_res = lib.execute(
            ['gcc', '-std=' + self.std, '-o', self.outfile, c_path])
        if compile_res['returncode'] == 0:
            res['success'] = True
            if compile_res['stderr']:
                res['compile_warnings'] = compile_res['stderr']
        else:
            res['success'] = False
            res['compile_error'] = compile_res['stderr']

        return res

    def _clean(self):
        if self.outfile:
            try:
                os.remove(self.outfile)
            except FileNotFoundError:
                pass
        self.outfile = None
                


def main():
    with CCompiler() as c:
        for key, value in c.compile('example.c').items():
            print(key.center(80, '-'))
            print(value)


if __name__ == '__main__':
    main()
