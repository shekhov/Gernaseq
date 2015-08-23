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

    @unittest.skip
    def testHelpCalled (self):
        """ Test Error. Argument -h or help should cause System exit """
        self.assertRaises(SystemExit, fastqc_reports.main, ("-h", ""))
        self.assertRaises(SystemExit, fastqc_reports.main, ("--help", ""))

    def testWrongInputPath (self):
        """Test Error. Path should exist as a directory"""
        self.assertRaises(fastqc_reports.InputError, fastqc_reports.main, ("-i", "poo"))

    def testZipFiles (self):
        """Test Error. Directory should contain at least one .zip file if -z argument was passed"""
        self.assertRaises(fastqc_reports.TypeError, fastqc_reports.main, ("-z", "-i", "src"))

    def testWrongFileExtention (self):
        """Test Error. Given name should be with .csv extention"""
        self.assertRaises(fastqc_reports.InputError, fastqc_reports.main, ("-f", "poo.bar"))

if __name__ == '__main__':
    unittest.main()
