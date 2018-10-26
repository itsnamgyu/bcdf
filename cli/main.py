import sys
sys.path.append('..')

import os
import glob
import re
from collections import defaultdict
import json
import codecs
import shutil

import pandas as pd

import lib
from core import case
from core import tester
from core import compiler as cp
from load.lib import auto_open

while True:
    try:
        n_problems = int(input('how many problems: '))
        break
    except ValueError:
        pass

sources = glob.glob('source/*.c')
key_re = re.compile('(20[0-9]{6})')

sources.sort()
students = defaultdict(list)

for source in sources:
    match = key_re.search(source)
    students[match.group(1)].append(source)

print('Source Files By Student'.center(100, '-'))
print(json.dumps(students, indent=4))

testsets = []
answersets = []
for _ in range(4):
    testsets.append(list())
    answersets.append(list())

while True:
    s = input('Add test case? {}, q: '.format(list(range(0, n_problems + 1))))
    if s == 'q':
        break
    else:
        try:
            testset = testsets[int(s) - 1]
            answerset= answersets[int(s) - 1]
        except:
            continue

    string = lib.edit_string()
    test = case.StdInputTest(string)
    testset.append(test)

    answer = lib.edit_string(title="answer")
    answerset += answer.split()
    
    print('Test Cases by Program'.center(100, '-'))
    for i, tests in enumerate(testsets):
        print('Program {:2d}: {:2d}'.format(i + 1, len(tests)))


results = pd.DataFrame(columns=list(range(n_problems)), index=students.keys())
results.index.name = 'student_id'

try:
    for i in range(n_problems):
        for key, sources in sorted(students.items()):
            print('\n' * 5)
            print('{} - Program {}'.format(key, i + 1).center(100, '*'))
            print()
            try:
                source = sources[i]
            except:
                print('NO SOURCE')
            with auto_open(source) as f:
                print('Source'.center(100, '-'))
                print(f.read())

            with cp.CCompiler() as c:
                cres = c.compile(source)
                if cres['success']:
                    res = tester.Tester().run(cres['executable'], testsets[i])
                    outputset = []
                    for r in res:
                        outputset += r['stdout'].split()

                    if outputset == answersets[i]:
                        print('CORRECT!')
                    else:
                        for j, r in enumerate(res):
                            if len(r['stdout']) > 1000:
                                r['stdout'] = r['stdout'][:1000] + '... total of {} chars'.format(len(r['stdout']))

                            print('Input {}'.format(j + 1).center(100, '-'))
                            print(r['stdin'])

                            print('Output {}'.format(j + 1).center(100, '-'))
                            print(r['stdout'])

                            if r.get('stderr'):
                                print('Stderr {}'.format(j + 1).center(100, '-'))
                                print(r['stderr'])
                    print('All Results'.center(100, '-'))
                    print(json.dumps(res, indent=4))
                else:
                    print('Compile Error'.center(100, '-'))
                    print(cres['compile_error'])
            ho = input('Score: ')
            results.loc[key, i] = ho
except:
    pass
finally:
    if os.path.isfile('results.csv'):
        shutil.copyfile('results.csv', 'results.csv.bak')
    results.to_csv('results.csv')
