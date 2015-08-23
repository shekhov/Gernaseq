__author__ = 'Anton Shekhov'
import unittest
import getopt
import sys
import os.path

# Spend two hours to figure this shit out!!!
sys.path.append  (os.path.abspath("./"))
from src import fastqc_reports

class FastqcTestCase (unittest.TestCase):
    """ Test of the fastqc report merging tool"""
    def testInputZero (self):
        """ Should give a message about usage """

    def testWrongInputPath (self):
        """Path should exist"""

    def testWrongFileExtention (self):
        """Given name should be with .csv extention"""

if __name__ == '__main__':
    unittest.main()
