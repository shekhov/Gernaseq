import argparse
import sys

def trimming (input_path, output_path, start, end, keep):

        input_file = open (input_path, 'r')
        output_file1 = open (output_path, "w")

        output_data = {}

        data = input_file.read().split ("\n")
        nseq = (len(data)-1)/2
        print ("Initial number of sequences were = ", nseq)
        count = 0
        keep_count = 0

        for i in range (len(data)-1):
                f = data[i] # name
                s = data[i+1] # sequence
                if ">" in f:
                        if len (s) >= end:
                                temp_s = s[start:end]   
                                output_data[f] = temp_s
                        else :
                                count += 1
                                if keep:
                                        output_data[f] = s
                                        keep_count += 1

        print (count , " sequences were less than ", end-start)
        if keep: print (keep_count, " sequences were kept, regardless their small length")
        print ("Final number of sequences is ", nseq-count)

        print ("Writing output file...")    
        for names, seq in output_data.items():
                output_file1.write (names + '\n')
                output_file1.write (seq + "\n")

        input_file.close()
        output_file1.close()

        print ("Done")
        input ("Enter to exit")     
        
def InputHandler (args):
        parser = argparse.ArgumentParser(description='Trim sequences to achieve desire length regardless to the quality'
                                                     'If the initial sequence line is less than END-START, do not include'
                                                     ' it into the outcome file. '
                                                     'This can be changed by setting flag --keep')
        parser.add_argument ("input", metavar="input.fasta", type=argparse.FileType('r'),
                             nargs="?", default="input.fasta",
                             help="Path to the sequence file in fasta format")
        parser.add_argument ("output", metavar =  "output.fasta", default="output.fasta",
                     type=argparse.FileType('w'),
                     help="Path to the output file with trimming sequences")
        parser.add_argument ("end", metavar="END", type=int,
                     help="The position of the right border in the frame. "
                          "When START is 0 (default), END is also a length of the frame")

        parser.add_argument ("-s", "--start", metavar="START", default=0, type=int,
                             help="The position of the left border in the frame (default: %(default)s)")
        parser.add_argument ("--keep", action="store_true",
                             help="Should the frames less than END-START be kept in the output file (default: %(default)s)")
        parser.add_argument ("--version", action='version', version='%(prog)s 0.1')
                        
        return (parser.parse_args())
        
def main (argv):
        input = InputHandler (argv)
        trimming (input.input, input.output, input.start, input.end, input.keep)
        
if __name__== "__main__":
        main (sys.argv[1:])