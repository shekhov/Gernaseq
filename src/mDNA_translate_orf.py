import sys
import os

class AminoAcidError (Exception): pass
class NoStopCodonError (AminoAcidError): pass

START_CODON = "AUG"

STOP_CODONS = ['UAG', 'UGA', 'UAA']

RNA_code = {
			'UCC': 'S',		'AUG': 'M',		'AUA': 'I', 	'CAA': 'Q', 	'AUC': 'I',
			'GUG': 'V', 	'GAG': 'E', 	'UAG': False, 	'GUC': 'V', 	'UCA': 'S',
			'GUA': 'V', 	'AUU': 'I', 	'UGC': 'C', 	'UCU': 'S', 	'UGU': 'C',
			'UAU': 'Y', 	'UCG': 'S', 	'GUU': 'V', 	'GCU': 'A', 	'UUC': 'F', 
			'ACA': 'T', 	'AGC': 'S', 	'GAA': 'E', 	'AGG': 'R', 	'GCG': 'A', 
			'GCA': 'A', 	'GCC': 'A', 	'GGA': 'G', 	'GGC': 'G', 	'ACC': 'T',
			'GGG': 'G', 	'UUA': 'L', 	'CAU': 'H', 	'CCU': 'P', 	'GGU': 'G',
			'UUG': 'L', 	'AAA': 'K', 	'UAA': False, 	'CGG': 'R', 	'CGA': 'R',
			'CGC': 'R', 	'ACU': 'T', 	'CAG': 'Q', 	'ACG': 'T', 	'CCC': 'P',
			'CAC': 'H', 	'UAC': 'Y', 	'CCG': 'P', 	'CGU': 'R', 	'AAC': 'N',
			'AAU': 'N', 	'CCA': 'P', 	'UGA': False, 	'CUU': 'L', 	'AGU': 'S',
			'CUC': 'L', 	'GAC': 'D', 	'CUA': 'L', 	'CUG': 'L', 	'GAU': 'D', 
			'UGG': 'W', 	'AAG': 'K', 	'AGA': 'R', 	'UUU': 'F'
			}


def find_all_start_codons (RNA):
	""" Return an array with indexes of AGU sequence"""
	result = []
	for n in range (len(RNA)):
		if RNA[n:n+3] == START_CODON:
			result.append (n)
	return (result)
	
def find_next_stop_codon (RNA):
	""" Codon (+3) dependant """
	id = 0
	while id < len(RNA):
		tRNA = RNA[id:id+3]
		if not tRNA in RNA_code: return False
		if RNA_code[tRNA] == False:
			return id
		id+= 3
	return False

def get_orf (RNA):
	""" Return array with indexes of open frames """
	result = []
	
	start_codons = find_all_start_codons (RNA)
	for codon in start_codons:
		next_stop = find_next_stop_codon (RNA[codon:])
		if not next_stop:
			if len(result) == 0: raise NoStopCodonError #Exit of no stop-codon in the whole sequence
			else: break #Exit if no more codons around
			
		result.append ([codon, codon + next_stop])
	return result

def return_peptide (RNA):
	""" Return correspondance peptide based on given RNA """
	# Should work with already made sequence without stop codons. Only one peptide per call

	peptide = ""
	id = 0
	while id < len(RNA):
		tRNA = RNA[id:id+3]
		if not tRNA in RNA_code: break
		AA = RNA_code[tRNA]
		if AA == False: # In the case if was mistake in the previous step
			break
		peptide += AA
		id += 3	
	return peptide

def translation (RNA):
	""" transform rna to corresponding peptides, start-stop codon dependant """
	result = []
	if len(RNA) == 0: return result

	orf = get_orf(RNA)

	for frame in orf:
		peptide = return_peptide(RNA[frame[0]:frame[1]])
		result.append(peptide)
	return result

def main (argv):
	input_folder = argv[0]
	output_folder = argv[1]
	
	# Check if the folder for output exists
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
		
	files = os.listdir (input_folder)	
	
	print ("Input folder contains " + str (len (files)) + " files.")
	
	for f in files:
		print ("Open " + str(f) + " file. ")
		input_path = os.path.join (input_folder, f)
		output_path = os.path.join (output_folder, f)

		input_file = open (input_path, 'r')
		output_file = open (output_path, "w")

		# Depends on how file look liked
		data = input_file.read().split (">")[1:]

		print ("------> ", "File contains " + str(len(data)) + " sequences.")

		result = {}

		for d in data: 
			# Name of the gene is a first
			# Sequence is the rest
			name = ">"+d.split("\n")[0]
			# Names should be unique. The script does not check for it
			seq = "".join(d.split("\n")[1:])
			rna = seq.replace('T', 'U')
			rev_rna = rna[::-1]
			proteins = translation (rna) + translation(rev_rna)
			# Magic line. Does the same as in R which.max
			bigest = (max (proteins, key=len))
			result[name] = bigest

		print ("------> ", str(len(result)) + " proteins translated.")

		print ("------> ","Write to file...")
		for key, value in result.items(): 
			output_file.write (key + "\n")
			output_file.write (value + "\n")
		print ("------> ","Done!")

		input_file.close()
		output_file.close()
	
        
if __name__== "__main__":
        main (sys.argv[1:])
