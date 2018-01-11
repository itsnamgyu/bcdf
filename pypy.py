from chardet.universaldetector import UniversalDetector
import codecs
import glob
import os
import re


def get_encoding(file):
    detector = UniversalDetector()
    for line in open(file, "rb"):
        detector.feed(line)
        if detector.done: break
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

# Get the output string of a python progam for a given input string
def get_output(py_source, input_string):
    os.system("touch temp")
    os.system("echo \"{}\" | python3 \"{}\" >> temp".format(input_string, py_source))
    with codecs.open("temp", mode="r", encoding="utf-8") as f:
        output_string = f.read()
    os.remove("temp")
    return output_string


# Get the dict of file outputs from a python program for a given dict
# of file inputs
# file_input example:      { "in0.txt": "12/12", "in1.txt": "23/21" }
# output_files example:    [ "out0.txt", "out1.txt" ]
# return example:          { "stdout": "Done", "out0.txt": "December 12th", "out1.txt": "Error" }
def get_file_output(py_source, file_input, output_files, input_string = ""):
    output = {}

    for file in file_input:
        with open(file, "w") as f:
            f.write(file_input[file])
    os.system("rm temp")
    os.system("echo \"{}\" | python3 \"{}\" >> temp".format(input_string, py_source))
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

# All Korean text files made with notepad are encoded in Korean (Windows, DOS)
#
# This function recursively searches a directory for all files of a given list
# of extensions and fixes their encoding to utf-8
def fix_all_encoding(directory = ".", extension_list = [ ".txt" ]):
    files = [ file for file in glob.glob(directory + "/**/*" + ext) + glob.glob(directory + "/*" + ext) for ext in extension_list ]
    invalid_files = []
    for file in files:
        if not fix_encoding(file):
            invalid_files.append(file)
    print("Invalid Files:")
    for file in invalid_files:
        print(file)
                    

# Generates a grader function that shows the human grader the original source
# code and output for a given input string, and asks for the grade and comments
def generate_manual_grader(input_string):
    def manual_grader(py_source, outfile):
        print("FILENAME: {}".format(py_source));
        print("PYTHON SOURCE")
        with open(py_source, "r") as sourcefile:
            source = sourcefile.read()
        print(source)
        print("OUTPUT")
        print(get_output(py_source, input_string))
        score = input("Enter score")
        comments = input("Enter comments")
        outfile.write("{},{},{}\n".format(py_source, score, comments))
    return manual_grader

# An example of a custom automatic grader function
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
        print("OUTPUT")
        print("-" * 60)
        print(output)
        print("-" * 60)
        if input("Is this output invalid? (any character for invalid)"):
            print("Invalid output")
        points -= 50

    if points == 100:
        print("Perfect")
    outfile.write("{},{}\n".format(py_source, points))
    
# Recursively searches for all python files within a directory and calls the
# grader function. The grader function is given two parameters: (1) the python
# source path and (2) the file stream to a report card file
def iterate_py(directory = ".", grader = generate_manual_grader(""), report_card = "results.csv"):
    with open(report_card, "w") as f:
        for py_source in glob.glob(directory + "/**/*.py") + glob.glob(directory + "/*.py"):
            if py_source != "./{}".format(__file__):
                print("{:*^80}".format(py_source))
                grader(py_source, f)
    print("*" * 80)
    print("Done.")

def main():
    #iterate_py(grader = generate_manual_grader(input_string))
    iterate_py(grader = ex_auto_grader)

if __name__ == "__main__":
    main()
