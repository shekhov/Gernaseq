__author__ = 'Anton Shekhov'

import unittest
import sys
import os
#import argparse

sys.path.append  (os.path.abspath("./"))
sys.path.append (os.path.abspath("../"))
from src import trim_length

class TrimLengthCase (unittest.TestCase):
        def setUp(self):
                self.input = os.path.join("tests", "testing_files", "trim_length.fasta")
                self.output = os.path.join("tests", "testing_files", "temp.fasta")
                self.end = 20
                self.start = 2
                self.first_0_20 = "AAAAAAAAAAAAAAAAAAAA"
                self.first_2_20 = "AAAAAAAAAAAAAAAAAAAA"
                self.second_0_20 = "TTTTCTTTTTTTTTTTTTTT"
                self.second_2_20 = "TTCTTTTTTTTTTTTTTTTT"
                self.third_0_20_keep = "ATACTA"
                self.third_2_20_keep = "ATACTA"
        def testInputHandler (self):
                """
                Check returning arguments
                """
                args = [self.input, self.output , '20']
                result = trim_length.InputHandler(args)

                self.assertEqual (result.input, self.input)
                self.assertEqual (result.output, self.output)
                self.assertEqual (result.end, 20)

        def testOutputFile (self):
                """
                Check correct output
                """
                args_first = [self.input, self.output, self.end]
                args_second = [self.input, self.output, self.end, "-s", self.start]
                first_trim = trim_length.trimming(self.input, self.output, self.end, quiet=True)




if __name__ == '__main__':
        unittest.main()