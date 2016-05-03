import sys
import os
import logging
logging.basicConfig(filename="log_trim_condition.txt", 
					format='%(asctime)s %(message)s', level=logging.INFO)

###################################
### CHANGE FOLLOWING PARAMETERS ###
###################################

# Do we want to keep fasta formating? 100 leters per string
keep_fasta = True

# Write down how do you wanna check every sequence
def check (seq):
	# Write here your conditions 
	if (len (seq) < 350) | (len (seq) > 550):
		return False
	else: 
		return True

################################
### NOW SAVE FILE AND TYPE 	 ###
### python trim_condition.py ###
###	Enjoy results :D 	  	 ###
################################

def log (msg):
	print (msg)
	logging.info (msg)

def main (argv):
	input_folder = argv[0]
	output_folder = argv[1]
	
	log ("\n---------------------------\nArguments are: " + ", ".join (argv) + "\n---------------------------")

	
	# Check if the folder for output exists
	if not os.path.exists(output_folder):
		log ("Create an output folder")
		os.makedirs(output_folder)
		
	files = os.listdir (input_folder)	
	
	log ("Input folder contains " + str (len (files)) + " files.")
	
	for f in files:	
		log ("Open " + str(f) + " file. ")
		input_path = os.path.join (input_folder, f)
		output_path = os.path.join (output_folder, f)

		input_file = open (input_path, 'r')
		output_file = open (output_path, "w")

		# Depends on how file look liked
		data = input_file.read().split (">")[1:]

		log ("File contains " + str(len(data)) + " sequences.\n")

		result = {}
		for d in data: 
			# Name of the gene is a first
			# Sequence is the rest
			name = ">"+d.split("\n")[0]
			# Names should be unique. The script does not check for it
			seq = "".join(d.split("\n")[1:])
			if check (seq):
				if keep_fasta: result[name] = "\n".join(d.split("\n")[1:])
				else: result[name] = seq 

		log (str(len(result)) + " of which are match given conditions.")

		log ("Write to file...")
		for key, value in result.items(): 
			output_file.write (key + "\n")
			output_file.write (value + "\n")
		log ("Done!\n")

		input_file.close()
		output_file.close()

if __name__== "__main__":
        main (sys.argv[1:])
