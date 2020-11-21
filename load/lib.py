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


def auto_read(path):
    default_codecs = ["EUC-KR", "ISO-8859-9", "CP949"]  # Korean stuff

    try:
        with codecs.open(path, 'r') as f:
            return f.read()
    except UnicodeDecodeError:
        pass

    for codec in default_codecs:
        try:
            with codecs.open(path, 'rU', codec) as f:
                return f.read()
        except UnicodeDecodeError:
            pass

    return None


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
