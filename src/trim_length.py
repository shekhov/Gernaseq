import argparse
import sys

def trim (input_dic, end, start=0, keep=False, quiet=False):
        count = 0
        keep_count = 0
        
        output_data = []
        
        for i in range (len(input_dic)-1):
                f = input_dic[i] # name
                s = input_dic[i+1] # sequence
                if ">" in f:
                        if len (s) >= end:
                                temp_s = s[start:end]   
                                output_data.append([f, temp_s])
                        else :
                                count += 1
                                if keep:
                                        output_data.append([f, s])
                                        keep_count += 1
        if not quiet:
                print (count , " sequences were less than ", end-start)
                if keep: print (keep_count, " sequences were kept, regardless their small length")
                print ("Final number of sequences is ", nseq-count)
                print ("Writing output file...")  
     
        return output_data

def trimming (input_path, output_path, end, start=0, keep=False, quiet=False):

        input_file = open (input_path, 'r')
        output_file1 = open (output_path, "w")

        data = input_file.read().split ("\n")
        nseq = (len(data)-1)/2

        if not quiet: print ("Initial number of sequences were = ", nseq)

        output_data = trim (data, end, start, keep, quiet)

        for names, seq in output_data:
                output_file1.write (names + '\n')
                output_file1.write (seq + "\n")

        input_file.close()
        output_file1.close()

        if not quiet:
                print ("Done")
                input ("Enter to exit")
        
def InputHandler (args):
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                         description='Trim sequences to achieve desire length regardless to the quality'
                                                     'If the initial sequence line is less than END-START, do not include'
                                                     ' it into the outcome file. '
                                                     'This can be changed by setting flag --keep',
                                         epilog="""Note that unique line identifications (begin with > sign
                                                 in fasta format) will not be suppressed. They are handled as a separate
                                                sequences. To delete non-unique lines run trim_unique.py script""")
        #TODO: make trim_unique.py script
        # Positional agruments
        parser.add_argument ("input", metavar="input.fasta",
                             nargs="?", default="input.fasta",
                             help="Path to the sequence file in fasta format")
        parser.add_argument ("output", metavar =  "output.fasta", default="output.fasta",
                             nargs="?",
                             help="Path to the output file with trimming sequences")
        parser.add_argument ("end", metavar="END", type=int, nargs='?',
                             help="The position of the right border in the frame. "
                                  "When START is 0 (default), END is also a length of the frames")

        # Optional arguments
        parser.add_argument ("-s", "--start", metavar="START", default=0, type=int,
                             help="The position of the left border in the frame ")#(default: %(default)s)")
        parser.add_argument ("--keep", action="store_true",
                             help="Should the frames less than END-START be kept in the output file (default: %(default)s)")
        parser.add_argument ("--version", action='version', version='Script %(prog)s v0.1')
        parser.add_argument ("-q", "--quiet", action="store_false",
                             help="Do not produce output")
                        
        return (parser.parse_args(args))
        
def main (argv):
        input = InputHandler (argv)
        trimming (input.input, input.output, input.end, input.start,input.keep, input.quiet)
        
if __name__== "__main__":
        main (sys.argv[1:])