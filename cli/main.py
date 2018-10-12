import sys
sys.path.append('..')

import os
import glob
import re
from collections import defaultdict
import json

import pandas as pd

import lib
from core import case
from core import tester
from core import compiler as cp

n_problems = 4

sources = glob.glob('source/*.c')
id_re = re.compile('(20[0-9]{6})')

sources.sort()
students = defaultdict(list)

for source in sources:
    match = id_re.search(source)
    students[match.group(1)].append(source)

print('Source Files By Student'.center(100, '-'))
print(json.dumps(students, indent=4))

testsets = []
for _ in range(4):
    testsets.append(list())

while True:
    s = input('Add test case? (1, 2, 3, 4, q) ')
    if s == 'q':
        break
    else:
        try:
            testset = testsets[int(s) - 1]
        except:
            continue
    
    string = lib.edit_string()
    testset.append(case.StdInputTest(string))

    for i, tests in enumerate(testsets):
        print('Test Cases [{}]'.format(i + 1).center(100, '-'))
        for j, test in enumerate(tests):
            print('[{}] {}...'.format(j + 1, test.get_stdin().splitlines()[0]))
    print('-' * 100)


results = pd.DataFrame(columns=list(range(n_problems)), index=students.keys())
results.index.name = 'student_id'

for i in range(n_problems):
    for key, sources in sorted(students.items()):
        print('\n' * 5)
        print('{} - Program {}'.format(key, i).center(100, '*'))
        print()
        try:
            source = sources[i]
        except:
            print('NO SOURCE')
        with open(source) as f:
            print('Source'.center(100, '-'))
            print(f.read())

        with cp.CCompiler() as c:
            cres = c.compile(source)
            if cres['success']:
                res = tester.Tester().run(cres['executable'], testsets[i])
                for j, r in enumerate(res):
                    print('Output {}'.format(j).center(100, '-'))
                    if len(r['stdout']) > 1000:
                        r['stdout'] = r['stdout'][:1000] + '... total of {} chars'.format(len(r['stdout']))
                    print(json.dumps(r, indent=4))
            else:
                print('Compile Error'.center(100, '-'))
                print(cres['compile_error'])
        ho = input('Score: ')
        results.loc[key, i] = ho

results.to_csv('results.csv')
