import os
import sys
import csv
import argparse
#import getopt
# Python 2.7

class Error (Exception):
        """Base error for this module"""
        pass

class InputError (Error):
        """ Exceptions raised when input was wrong
                Attributes:
                        msg -- explanation of the error
        """
        def __init__(self, msg):
                self.msg = msg
                pass

#TODO: Transfer input handler to argparse package
def input_handler2 (argv):
        inputFolder=""
        outputFolder=""
        outputFile=""
        rangeN=[]
        def Usage ():
                errorMSG="Usage:\npython combine_velvet_reports.py -i <inputFolder> " \
                        "-o <outputFolder> -f <filename> -r <rangeNumbers> -h" \
                                 " for help"
                print (errorMSG)
                sys.exit()

        try:
                opts, rest = getopt.getopt (argv, 'ho:r:f:i:', ["help", "outputFolder=", "rangeNumbers=", "inputFolder="])
        except getopt.GetoptError:
                Usage()

        for opt, arg in opts:
                #TODO help: Update. Version of Python
                if opt in ("-h", "--help"):
                        print ("\n\tCombine reports from velvet assembly to a single .csv table")
                        print ("Usage: \tpython combine_velvet_reports.py -i <inputFolder> -o <outputFolder> -r <rangeNumbers>")
                        print ("Arguments: ")
                        print ("\t-r (--rangeNumbers)two odd numbers with dash between them representing minimum and maximum value of the range to scan")
                        print ("\t-i (--inputFolder) a location of folders where assemblies are located")
                        print ("\t-o (--outputFolder) A specified location for the output file. If not specified, the default file report will be created in the folder where script was called")
                        print ("\t-f (--filename) A name of the report file with extention (.csv). Default name is velvet_report_<range>.csv")
                        sys.exit(2)

                elif opt in ("-i", "--inputFolder"):
                        path = os.path.join(os.getcwd(), arg)
                        if os.path.isdir (path) == True:
                                inputFolder = path
                        else: raise InputError (path+ " is not a directory")

                elif opt in ("-o", "--outputFolder"):
                        outputFolder = arg

                elif opt in ("-f", "--filename"):
                        if arg[-3:] == 'csv':
                                outputFile = arg                        
                        else: raise InputError ( "Wrong file type was given. Read help")
                        #print ("Arg: ", arg, " OUT: ", outputFile)
                elif opt in ("-r", "--rangeNumbers"):
                        #print (arg)
                        if "-" in arg:
                                t = arg.split ("-")
                                #print (t)
                                rangeN.append(int(t[0])); rangeN.append (int(t[1]))
                        else: raise InputError ("Wrong range syntax given. Use - between numbers")

        if len (inputFolder) == 0: raise InputError ("no argument for Input folder was given")
        if len(outputFolder) == 0: outputFolder = os.getcwd()
        if len(rangeN) == 0: raise InputError ("No range of numbers was given")
        if len(outputFile) == 0: outputFile = "velvet_report_"+str(rangeN[0])+"-"+str(rangeN[1])+".csv"

        return {'i':inputFolder, 'o':outputFolder, 'f':outputFile, 'r':rangeN}

def input_handler (args):
        def range_numbers (string):
                #print (string + "pOOOO")
                if '-' not in string:
                        msg = "Range does not have - sign"
                        raise argparse.ArgumentTypeError (msg)
                else:
                        result = [int(x) for x in string.split("-")]
                        if len (result) != 2:
                                msg = "Wrong range format was given"
                                raise argparse.ArgumentTypeError (msg)
                        return result
                        
        
                        
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                         description='Combine reports from velvet assembly to a single .csv table')
        
        # argparse can't handle empty strings
        if len(args) < 1: raise argparse.ArgumentTypeError ("Read help")
                                         
        parser.add_argument ("-i", "--input", metavar="INPUT_FOLDER", nargs="?", default=os.getcwd(), help = "Path to the folder where assemblies are located")
                
        parser.add_argument ("range", metavar="MIN-MAX", nargs="?", type=range_numbers, help="two odd numbers with dash between them representing minimum and maximum value of the range to scan")
        
        parser.add_argument ("-o", "--output", metavar="OUTPUT_FILE", nargs="?", default="velvet_report_MIN-MAX.csv", help = "Name of the output file in csv format.")

        
        parser.add_argument ("-f", "--folder", metavar="OUTPUT_FOLDER", default=os.path.join (os.getcwd()), help = "Path to the folder, where output file will be created. Default is the folder you called a script from.") 

        
        result = parser.parse_args(args)
        # Finishing 
        if result.output == 'velvet_report_MIN-MAX.csv': 
                result.output = 'velvet_report' + "_" + str(result.range[0]) + "-" + str(result.range[1]) + ".csv"
        
        
        return result
        

def writeReports (input_folder, nRange, oWriter):
        for i in range (nRange[0], nRange[1], 2):
                path = os.path.join (input_folder, str(i), "Log")
                print ("Trying to open file", path)
                logfile = open(path, 'r')
                log = logfile.read().split ("\n")        
                o = [i]
                for l in log:
                        if "Final" in l: # result of velveth
                                print (l)
                                # Parse
                                n50line=l.replace(",","").split()
                                for j in range (len(n50line)):
                                        s=n50line[j]
                                        #nextL = n50line[j+1]
                                        if s == 'has' or s == 'of' or  s == 'max' or s == 'total':
                                                nextL = n50line[j+1]
                                                o.append ( int(nextL))
                        elif "Finished" in l: #result of oases
                                print (l)
                                lociLine = l.split (" ")
                                for j in range (len(lociLine)):
                                        if lociLine[j] == 'on': o.append (int (lociLine[j+1]))
                oWriter.writerow (o)	
                logfile.close()  

def prepareTemplate (path):
        """ Open csv file and create headers """
        output = open (path, 'w')
        oWriter = csv.writer (output)
        oWriter.writerow (['kmer', 'nodes', 'n50', 'max', 'total', 'loki'])
        return (output, oWriter)

def main (argv):
        input = input_handler (argv)
        output, oWriter = prepareTemplate (os.path.join(os.folder, os.output))
        writeReports (input.input, input.range, oWriter)
        output.close()

if __name__== "__main__":
        main (sys.argv[1:])