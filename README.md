![Language](https://img.shields.io/badge/Language-Python3.6-blue.svg)
![Document](https://img.shields.io/badge/Document-English-black.svg)

# bdcf
A auto-grading module to help TA's slack on the job! Our main language will be Python 3.

# Undergoing Major Construction

# Use case (contributors, plz read)

At Sogang University, this is usually what happens:

Students send in their assignments via email or the online campus site. We manually download them and put them into a directory. Often times, there is an issue with unicode encoding (when the filenames contain Korean). About a quarter of the filenames are in the incorrect format.

Then, we grade the assignments one-by-one. In my case, I use a auto-renaming program to fix the filenames, then write a short Python snippet to grade the assignments.

Once we're done, we have to fill in a proprietary spreadsheet handed to us by the *upper managers*. It may or may not require us to fill in the details of the results, i.e., reasons for each deduction.

## What we'll do...
This is what our program will do:
1. Identify the source code path and the owner
  - To deal with issues with filenames, we'll just extract identifiers like student id.
  - Some assignments may contain multiple exercises. In this case, we just order the path names in lexicographical order and put indices on them.
2. Compile and run with stdin, file input, stdout and file output
  - We will need to support multiple test cases
  - We will start with the simple features first. For example, start out with output visualization, then move on to auto-comparisons.

## Priorities
- Readability over development speed over optimizaiton.
- Consider the ROI for the *TA* who is using this program. For instance: copy-checking feature—that's a *want*, not a *need*.
- On the subject of ROI, note that the more you want to automate, the more exceptions you'll need to deal with.
- We're trying to make like easier for the TA. We want 99% of hand-ins to be covered *bcdf*.

## What we won't do...
We will not come up with a whole new workflow for students to send in their assignments. We do not want to liable for any issues there. Not to mention, convincing the school board, professors, TA managers to change the system is just a bit cumbersome. I imagine that's not very comfortable for us shy, gitty CSE majors. Let's just get the job done, *get dat TA money, get some coffee, and get on with our own assignments.*

![Get dat TA money](https://media.giphy.com/media/gTURHJs4e2Ies/giphy.gif)

## We shall consider...
- Incorrect file formats (obviously)
- Situations when we need to use a makefile
- Multiple languages (let's just assume C, C++, Python for now)
