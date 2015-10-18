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
                self.output2 = os.path.join("tests", "testing_files", "temp2.fasta")
                self.end = 20
                self.start = 2
                self.first_0_20 = "AAAAAAAAAAAAAAAAAAAA"
                self.first_2_20 = "AAAAAAAAAAAAAAAAAA"
                self.second_0_20 = "TTTTCTTTTTTTTTTTTTTT"
                self.second_2_20 = "TTCTTTTTTTTTTTTTTT"
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

        def testOutputFileNoKeep (self):
                """
                Check correct output
                """
                # First trimming from 0 to 20 without keeping
                trim_length.trimming(self.input, self.output, self.end, quiet=True)

                output = open (self.output, 'r')
                o_lines = output.read().split("\n")
                self.assertEqual(len(o_lines), 5)
                self.assertEqual (o_lines[1], self.first_0_20)
                self.assertEqual(o_lines[3], self.second_0_20)
                output.close()
                os.remove(self.output)

        def testOutputFileKeep (self):
                """
                Check all keeping sequences and also shorter lines
                """

                # Second trimming from 2 till 20
                trim_length.trimming(self.input, self.output2, self.end, start=2, keep=True, quiet=True)
                output = open (self.output2, 'r')
                o_lines = output.read().split("\n")
                self.assertEqual(len(o_lines), 7)
                self.assertEqual(o_lines[1], self.first_2_20)
                self.assertEqual (o_lines[3], self.second_2_20)
                self.assertEqual (o_lines[5], self.third_2_20_keep)
                output.close()
                os.remove(self.output2)

if __name__ == '__main__':
        unittest.main()