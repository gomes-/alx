#!/usr/bin/env python3
#Bug: cmd gets broken down when passed to alx

__author__ = 'Alex Gomes'

import unittest, subprocess, os, sys

path_file = os.path.abspath(__file__)
dir_path = os.path.dirname(path_file)
dir_top = os.path.split(dir_path)[0]
sys.path.insert(0, dir_top)


class TestCase():
    def __init__(self, arg, name, case):
        self.arg = arg
        self.name = name
        self.case = case


class CMDTest():
    def __init__(self):
        global  dir_top
        self.dir_bin = os.path.join(dir_top, 'bin', 'alx')



    def run_test(self, testCase):
        case= "python {0} {1}".format(self.dir_bin, testCase.case)

        result = self.Execute(case)

        print("{0} , {1}, {2}, {3}\n".format(result, testCase.arg, testCase.name, case))


    def Execute(self, code):
        if subprocess.call(code, shell=True) == 0:
            return True;
        return False;


if __name__ == "__main__":
    test = CMDTest()

    cases = [TestCase("save", "Save a command", "save 'touch test1.txt' -n test1"),
             TestCase("run", "Save & Run command", "run 'touch test2.txt' -n test2")
             ]
    for case in cases:
        test.run_test(case)
