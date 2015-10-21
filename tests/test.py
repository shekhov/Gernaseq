__author__ = 'Anton Shekhov'
import unittest
import os.path
import sys

sys.path.append  (os.path.abspath("./"))
sys.path.append (os.path.abspath("../"))

# unittest declaration
import tests._fastqc_reports_test
import tests._trim_length_test
import tests._combine_velvet_reports_test

def __suite ():
        suite = unittest.TestSuite()

        suite.addTest(unittest.makeSuite(tests._fastqc_reports_test.FastqcTestCase))
        suite.addTest(unittest.makeSuite(tests._trim_length_test.TrimLengthCase))
        suite.addTest(unittest.makeSuite(tests._combine_velvet_reports_test.VelvetTestCase))

        return suite

if __name__ == '__main__':
        v = None
        if len (sys.argv[1:]) != 0: v = int (sys.argv[1:][0])
        if not v: v = 1
        unittest.TextTestRunner(verbosity=v).run(__suite())
