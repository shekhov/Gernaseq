Gernaseq
===============================================================================
Gernaseq is a library of scripts which are from the category: easier to make than look for tool which do the same. 
Scripts are located in the scr folder. 
* *trim_length.py*
  * Trim fasta/fastq sequence files by given window length. Can drop lines with a length smaller then given window
* *combine_velvet_reports.py*
  * Combine reports from velvet assembly LOG files to a single .csv table.
* *fastqc_reports.py*
  * Combine reports from fastqc tool into single .csv table.
* *tophatic.sh*
  * A bash script that can implement given command over a set of files.
* *mDNA_translate_orf.py*
  * Chooses the longest open reading frame from mDNA and translate it to AA sequence. 
  	* Input parameters are: 
 		* input_folder - the location of a folder where multiple fasta files with DNA sequences are
    	* output_folder - the location (will create folder if not exists) of a folder where output will go. Files will be created with the same name as input.

Licence
===============================================================================
All the scripts are free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


Author
===============================================================================
I am a PhD student at the [Max Planck Institute for Chemical Ecology] (http://ice.mpg.de), in Jena, Germany, studying insect/plant biochemistry
