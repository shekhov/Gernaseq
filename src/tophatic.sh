#! /bin/bash

show_help() {
cat << EOF
This script will work only if all names of the fastq files following one pattern.
To begin, type: 
	bash tophatic.sh <tophat2 command>
		-o OutputFolder/<%_SomeID> 		# For each input file one folder will be created
		-p 16 					# Number of threads to use 
		ReferenceFolder/<NameOfGenome without extention> # Usually this was created after bowtie2-build command 
		%_R1.fastq.gz %_R2.fastq.gz  		# Location of input files

Where % sign is the identificator of the treatment (i.e. just letter) and everything else after depends on the file you are using.
Script will look to the input files and if %_R1 and %_R2 match, it will run tophat command.
EOF
}

args="$@"

if [ ${#args} -eq 0 ]; then
	show_help
	exit
elif [[ $args == *"help"* ]]; then
	show_help
	exit
else
	printf 'The next command was given:\n-- %s \nTrying to implement\n' "$args"
	# Separate command line by % sign
	IFS=' ' read -a arr <<< "$args"
	len=${#arr[@]} # length of the array
	# Two last elements are the imput files
	inp1=${arr[len-2]}
	inp2=${arr[len-1]}

	# Position of % sign
	index1=`expr index "$inp1" %`
	#echo Index:"$index1"

	letters=()
	# Check this location
	IFS='%' read -a in1 <<< "$inp1"
	# Position of suffix, so we can cut letters
	index2=`expr index "$inp1" "${in1[1]}"`

	# Create variables of pattern
	for f in "${in1[0]}"*"${in1[1]}"; do
		#echo Indexes: "$index2" and "$index1" 
		letters+=("${f:index1-1:index2-1}"); done

	# Create commands for tophat based on letters we extracted
	for l in "${letters[@]}"; do 
		thisCommand=${args//%/$l}
		$thisCommand
	done

	#echo input1: "$inp1"
	#echo input2: "$inp2"
	# Going through all of them
	#for i in "${arr[@]}"; do
	#	echo "$i"
	#done
	# get list of the files on the input location
	exit
fi 

# End of file
# Made by Anton Shekhov
# sh.anton2111@gmail.com
