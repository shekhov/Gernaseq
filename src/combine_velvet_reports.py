import os
import sys
import csv
import argparse

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