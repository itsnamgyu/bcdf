import os
import codecs
import warnings

import chardet


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _get_encoding(b):
    return chardet.detect(b)['encoding']

def _get_encoding_from_file(path):
    with open(path, 'rb') as f:
        return _get_encoding(f.read())

def auto_open(path):
    encoding = _get_encoding_from_file(path)
    try:
        return codecs.open(path, 'rU', encoding)
    except UnicodeDecodeError:
        pass
    try:
        return codecs.open(path, 'r')
    except UnicodeDecodeError:
        warnings.warn("couldn't decode file. return empty file:\n{}".format(str(e)))
        return open(os.path.join(BASE_DIR, 'blank.txt'), 'r')

def auto_decode(b):
    if len(b) == 0:
        return ''

    encoding = _get_encoding(b)
    if encoding:
        try:
            return b.decode(encoding)
        except UnicodeDecodeError:
            pass

    try:
        return b.decode()
    except UnicodeDecodeError:
        warnings.warn("couldn't decode string. return empty string:\n{}".format(str(e)))
        return ''
