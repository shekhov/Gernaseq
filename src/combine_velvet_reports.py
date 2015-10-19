import os
import sys
import csv
import getopt
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
def input_handler (argv):
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

def writeReports (writer, input):
        for i in range (input['r'][0], input['r'][1], 2):
                path = os.path.join (os.getcwd(), input['i'], str(i), "Log")
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
                writer.writerow (o)	
                logfile.close()        

def main (argv):
        input = input_handler (argv)
        
        output = open (os.path.join (os.getcwd(), input['o'], input['f']), 'w')
        oWriter = csv.writer (output)
        oWriter.writerow (['kmer', 'nodes', 'n50', 'max', 'total', 'loki'])
        writeReports (oWriter, input)
        output.close()

if __name__== "__main__":
        main (sys.argv[1:])