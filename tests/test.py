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
                self.assertEqual (test_result['i'], path)
                self.assertEqual (test_result['o'], path)                

        def testListFiles (self):
                """Given folder should contain needable files"""
                # Test works only if calles from parent directory
                path = os.getcwd()
                no_files = os.path.join (path, "tests/no_files")
                zip_files = os.path.join (path, "tests/zip_files")
                folder_files = os.path.join (path, "tests/report_folders")
                
                # Error if empty folder is given
                self.assertRaises (fastqc_reports.TypeError, fastqc_reports.get_file_list, no_files, False)
                # Error if folder with no report .zip files
                self.assertRaises(fastqc_reports.TypeError, fastqc_reports.get_file_list, folder_files, True)
                # Error if folder without report folders
                self.assertRaises(fastqc_reports.TypeError, fastqc_reports.get_file_list, zip_files, False)
                
                # Return exact numbers of files in the folder
                self.assertEqual (len (fastqc_reports.get_file_list (zip_files, True)), 5)
                self.assertEqual (len (fastqc_reports.get_file_list (folder_files, False)), 3)
        
        def testZipRecognition (self):
                # Test is returning TRUE when -z parameter is given, and FALSE when not
                
                self.assertTrue (fastqc_reports.input_handler(("-z", ""))['z'])
                self.assertFalse (fastqc_reports.input_handler((""))['z'])

        def testWrongFileExtention (self):
                """Test Error. Given name should be with .csv extention"""
                self.assertRaises(fastqc_reports.InputError, fastqc_reports.input_handler, ("-f", "poo.bar"))
        
        def testFileParser (self):
                """ Should return dictionary """
                filePath = os.path.join (os.getcwd(), "tests", "report_folders", "001_f_fastqc", "summary.txt")
                f = open (filePath)
                result = fastqc_reports.parse_fastqc_summary (f, False)
                self.assertEqual (len(result), 12)
                self.assertEqual (result['Basic Statistics'], 'PASS')
                f.close()
                
        def testZipFileParser (self):
                """ Should return correct dictionary """
                filePath = os.path.join (os.getcwd(), "tests", "zip_files", "test_fastqc.zip")                
                result = fastqc_reports.get_info_from_zip (filePath)
                self.assertEqual (len(result), 12)
                self.assertEqual (result['Basic Statistics'], 'PASS')

if __name__ == '__main__':
        unittest.main()
