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
        def testInputHandler (self):
                """
                Check returning arguments
                """
                args = [self.input, self.output , '20']
                #args = ['tests\\testing_files\\trim_length.fasta', 'tests\\testing_files\\temp.fasta', '20']
                result = trim_length.InputHandler(args)
                self.assertEqual (result.input, self.input)
                self.assertEqual (result.output, self.output)
                self.assertEqual (result.end, 20)




if __name__ == '__main__':
        unittest.main()