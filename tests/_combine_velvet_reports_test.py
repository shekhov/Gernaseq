__author__ = 'Anton Shekhov'

import unittest
import sys
import os

sys.path.append  (os.path.abspath("./"))
sys.path.append  (os.path.abspath("../"))
from src import combine_velvet_reports as v

#TODO: make more tests before further development
class VelvetTestCase (unittest.TestCase):
        def testInputErrors (self):
                pass
                
        def testRightInput (self):
                i_path = os.getcwd()
                o_path = os.getcwd()
                #r_test = [1,5]
                r_test = "1-5"
                f_test = "velvet_report_1-5.csv"
                test_result = v.input_handler ([i_path, r_test, "-o", o_path]) 
                self.assertEqual (i_path, test_result.input)
                self.assertEqual (f_test, test_result.output_file)
                self.assertEqual (o_path, test_result.output)
                #self.assertEqual (f_test, test_result['f'])
                self.assertEqual (r_test, test_result.range)
                
        def testWritReport (self):
                pass
                

if __name__ == '__main__':
        unittest.main()