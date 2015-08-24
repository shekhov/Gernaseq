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
                self.assertRaises(SystemExit, fastqc_reports.input_handler, ("-h", ""))
                self.assertRaises(SystemExit, fastqc_reports.input_handler, ("--help", ""))

        def testInputPath (self):
                """Tests for input folder"""
                # Should give an error if not exit
                self.assertRaises(fastqc_reports.InputError, fastqc_reports.input_handler, ("-i", "poo"))
                # Test works only if calles from parent directory
                test_path = "src"
                path = os.path.join (os.getcwd(), test_path)
                test_result = fastqc_reports.input_handler (("-i", test_path))
                self.assertEqual (test_result['i'] == path)

        def testZipFiles (self):
                """Test Error. Directory should contain at least one .zip file if -z argument was passed"""
                # Test works only if calles from parent directory
                self.assertRaises(fastqc_reports.TypeError, fastqc_reports.test_files, ("-z", "-i", "src"))

        def testWrongFileExtention (self):
                """Test Error. Given name should be with .csv extention"""
                self.assertRaises(fastqc_reports.InputError, fastqc_reports.input_handler, ("-f", "poo.bar"))

if __name__ == '__main__':
        unittest.main()
