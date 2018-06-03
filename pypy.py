from chardet.universaldetector import UniversalDetector
import codecs
import glob
import os
import re
import argparse
import io
from typing import List, Dict, Tuple


# { output: (score, comment) }
result_dict: Dict[str, Tuple[str, str]] = {}


def get_all_pies(directory=".", only_subdirs=True):
    pies = glob.glob(directory + "/**/*.py", recursive=True)
    if not only_subdirs:
        pies += glob.glob(directory + "/*.py")
    return pies


def rename_py(directory="."):
    pattern = re.compile(r'2[0-9]{7}')
    for py in get_all_pies():
        dir, name = os.path.split(py)
        print(name)

        found = pattern.search(name)
        if found:
            student_num = found.group()
            new_py = os.path.join(dir, student_num + ".py")
            os.rename(py, new_py)
            print(name, student_num, new_py)


def get_encoding(file):
    detector = UniversalDetector()
    for line in open(file, "rb"):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']


def fix_encoding(file):
    encoding = get_encoding(file)
    try:
        with codecs.open(file, 'rU', encoding) as source_file:
            string = source_file.read()
        with codecs.open(file, 'w', 'utf-8') as target_file:
            target_file.write(string)
    except UnicodeDecodeError:
        return False
    return True


'''
Get the output string of a python progam for a given input string
'''


def get_output(py_source, input_string):
    os.system("touch temp")
    os.system("echo \"{}\" | python3 \"{}\" >> temp".format(
        input_string, py_source))
    with codecs.open("temp", mode="r", encoding="utf-8") as f:
        output_string = f.read()
    os.remove("temp")
    return output_string


'''
Get the dict of file outputs from a python program for a given dict
of file inputs
file_input example:      { "in0.txt": "12/12", "in1.txt": "23/21" }
output_files example:    [ "out0.txt", "out1.txt" ]
return example:          { "stdout": "Done", "out0.txt": "December 12th", "out1.txt": "Error" }
'''


def get_file_output(py_source, file_input, output_files, input_string=""):
    output = {}

    for file in file_input:
        with open(file, "w") as f:
            f.write(file_input[file])
    os.system("rm temp")
    os.system("echo \"{}\" | python3 \"{}\" >> temp".format(
        input_string, py_source))
    with io.open("temp", mode="r", encoding="utf-8") as f:
        output["stdout"] = f.read()
    io.remove("temp")

    for file in output_files:
        try:
            with open(file, "r") as f:
                output[file] = f.read()
        except:
            output[file] = ""

    return output


'''
All Korean text files made with notepad are encoded in Korean (Windows, DOS)
This function recursively searches a directory for all files of a given list
of extensions and fixes their encoding to utf-8
'''


def fix_all_encoding(directory=".", extension_list=[".txt"]):
    files = [file for file in glob.glob(
        directory + "/**/*" + ext) + glob.glob(directory + "/*" + ext) for ext in extension_list]
    invalid_files = []
    for file in files:
        if not fix_encoding(file):
            invalid_files.append(file)
    print("Invalid Files:")
    for file in invalid_files:
        print(file)


'''
Generates a grader function that shows the human grader the original source
code and output for a given input string, and asks for the grade and comments
'''


def generate_manual_grader(input_strings: List[str]):
    def manual_grader(py_source, outfile):
        print("{:-^60}".format("PYTHON SOURCE"))
        with open(py_source, "r") as sourcefile:
            source = sourcefile.read()
        print(source)

        total_output: str = ''
        for index, string in enumerate(input_strings):
            print("{:-^60}".format("OUTPUT {}".format(index)))
            output = get_output(py_source, string)
            print(output)
            total_output += output

        print("{:-^60}".format(""))
        if total_output in result_dict:
            score, comments = result_dict[total_output]
            print('same input: {}, {}'.format(score, comments))
        else:
            score = input("Enter score: ")
            comments = input("Enter comments: ")
            result_dict[total_output] = (score, comments)
        outfile.write("{},{},{}\n".format(py_source, score, comments))

    return manual_grader


def grader(py_source, outfile):
    input_string = \
        """13
1 0 -1 0 2 -2 -3 3 0 -4 4 0 0
"""
    re_code1 = re.compile(r".{0,}구[^`]{0,}다.{0,}")
    re_code2 = re.compile(r".+문제[^`]{0,}2[^`]{0,}")
    re_code_answer1 = re.compile(
        r"input[^`]{0,}while[^`]{0,}<[^`]{0,}:[^`]{0,}True")
    re_code_answer2 = re.compile(r"input[^`]{0,}split()[^`]{0,}\+[^`]{0,}1")
    re_out1 = re.compile(r"구[^`]{0,}다")
    re_out2 = re.compile(r".{0,}:.{0,}:.{0,}")
    re_answer1 = re.compile(
        r"2[^`]{0,}3[^`]{0,}5[^`]{0,}7[^`]{0,}11[^`]{0,}13[^`]{0,}17[^`]{0,}19[^`]{0,}23[^`]{0,}29[^`]{0,}31[^`]{0,}37[^`]{0,}41.{0,}\n.{0,}13")
    re_answer2 = re.compile(r":.{0,}4.{0,}:.{0,}4")

    with open(py_source, "r") as f:
        source = f.read()
    output = get_output(py_source, input_string)

    score = 10
    one = True
    two = True

    if not re_answer1.findall(output):
        out1 = re_out1.findall(output)
        print("{:-^60}".format("OUTPUT1"))
        if out1:
            print(out1[0])
        else:
            print(output)
        print("{:-^60}".format(""))

        if input("Wrong? (press anything for wrong)"):
            one = False
        else:
            one = False

    if one and not re_code_answer1.findall(source):
        code1 = re_code1.findall(source)
        print("{:-^60}".format("CODE1"))
        if code1:
            print(code1[0])
        else:
            print(source)
        print("{:-^60}".format(""))

        if input("Wrong? (press anything for wrong)"):
            one = False

    if not re_answer2.findall(output):
        out2 = re_out2.findall(output)
        print("{:-^60}".format("OUTPUT2"))
        if out2:
            print(out2[0])
        else:
            print(output)
        print("{:-^60}".format(""))

        if input("Wrong? (press anything for wrong)"):
            two = False
        else:
            two = False

    if two and not re_code_answer2.findall(source):
        code2 = re_code2.findall(source)
        print("{:-^60}".format("CODE2"))
        if code2:
            print(code2[0])
        else:
            print(source)
        print("{:-^60}".format(""))

        if input("Wrong? (press anything for wrong)"):
            two = False

    wrong = []
    if not one:
        score -= 1
        wrong.append(1)
    if not two:
        score -= 1
        wrong.append(2)

    print("SCORE: {}".format(score))
    outfile.write("{},".format(py_source))
    outfile.write(str(score) + ",")
    for n in wrong:
        outfile.write("{},".format(n))
    outfile.write("\n")


'''
An example of a custom automatic grader function
'''


def ex_auto_grader(py_source, outfile):
    points = 100
    with open(py_source, "r") as f:
        source = f.read()

    if not re.findall(r'input\(.+\)', source):
        print("No input function")
        points -= 50

    output = get_output(py_source, "12/12")
    if not re.findall(r'[Dd]ecember.{0,}12[Tt][Hh]', output):
        print()
        print("{:-^60}".format("OUTPUT"))
        print(output)
        print("-" * 60)
        if input("Is this output invalid? (any character for invalid)"):
            print("Invalid output")
        points -= 50

    if points == 100:
        print("Perfect")
    outfile.write("{},{}\n".format(py_source, points))


'''
Recursively searches for all python files within a directory and calls the
grader function. The grader function is given two parameters: (1) the python
source path and (2) the file stream to a report card file
'''


def grade(directory=".", grader=generate_manual_grader(['']), report_card="results.csv"):
    with open(report_card, "w") as f:
        py_sources = glob.glob(directory + "/**/*.py") + \
            glob.glob(directory + "/*.py")
        for py_source in py_sources:
            py_py_py = "./" + __file__  # pypy.py
            if py_source != py_py_py:
                print("{:*^80}".format(py_source))
                grader(py_source, f)
    print("*" * 80)
    print("Done.")


def main():
    parser = argparse.ArgumentParser(
        description='Grade your Python assignments... using Python!')
    parser.add_argument('-R', '--rename', action='store_true')
    parser.add_argument('-s', '--simple', action='store_true')
    parser.add_argument('-m', '--multistring', type=int)
    parser.add_argument('-d', '--directory', type=str)
    parser.add_argument('-r', '--results', type=str)
    args = parser.parse_args()

    if args.rename:
        if os.path.exists(args.rename):
            rename_py(directory=args.rename)
            return
        else:
            print("path '{}' does not exist".format(args.rename))

    directory = '.'
    if args.directory:
        if not os.path.exists(args.directory):
            print("path '{}' does not exist".format(args.directory))
            return
        else:
            directory = args.directory

    results = 'results.csv'
    if args.results:
        if args[:-4] == '.csv':
            results = args.results
        else:
            resutls = args.results + '.csv'

    if args.simple and args.multistring:
        print("can't enable both simple & multistring mode")
        return

    if args.simple:
        input_string = input('enter input string')
        grade(directory, grader=generate_manual_grader(
            [input_string]), report_card=results)

    if args.multistring:
        input_strings = []
        for i in range(args.multistring):
            input_strings.append(
                input('enter input string ({}/{})'.format(i + 1, args.multistring)))
        grade(directory, grader=generate_manual_grader(
            input_strings), report_card=results)


if __name__ == "__main__":
    main()
