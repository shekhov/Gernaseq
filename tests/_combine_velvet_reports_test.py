__author__ = 'Anton Shekhov'

import unittest
import sys
import os
import csv
import argparse

sys.path.append  (os.path.abspath("./"))
sys.path.append  (os.path.abspath("../"))
from src import combine_velvet_reports as v

#TODO: make more tests before further development
#TODO: Create test for writeReports method
class VelvetTestCase (unittest.TestCase):   

        def setUp (self):
                self.i_path = os.getcwd ()
                self.o_path = os.getcwd ()
                self.range_input = "1-5"
                self.range_res = [1,5]
                self.file_name = "velvet_report_1-5.csv"
                self.input_path = os.path.join (self.i_path, self.file_name)
                self.headers = ['kmer', 'nodes', 'n50', 'max', 'total', 'loki']

        def testTemplate (self):
                """ Check the headers for template creation """
                #input = v.input_handler (["-i", self.i_path, self.range_input, "-f", self.o_path])
                # Create file
                output, oWriter = v.prepareTemplate (path=self.input_path)
                output.close ()
                # Open this file
                test = open (self.input_path, 'r')
                reader = csv.reader (test)
                # Extract headers
                headers = reader.__next__()
                # Test it
                self.assertEqual (headers, self.headers)
                
                # close file and remove
                test.close()
                os.remove (self.input_path)
       
        def testRightInput (self):
                """ Test the argument parser """
                test_result = v.input_handler (["-i", self.i_path, self.range_input, "-f", self.o_path]) 
                self.assertEqual (self.i_path, test_result.input)
                self.assertEqual (self.file_name, test_result.output)
                self.assertEqual (self.o_path, test_result.folder)
                self.assertEqual (self.range_res, test_result.range)
        


if __name__ == '__main__':
        unittest.main()