
#####################################
#		 ABOUT THIS SCRIPY 			#
#####################################
# This script will read the results of sequenced samples of tissue
# so they can easily be searched and organized by the scientist.
# URL to retreive gene sequencing data for CCA tissue: https://tcga-data.nci.nih.gov/tcga/tcgaCancerDetails.jsp?diseaseType=CHOL&diseaseName=Cholangiocarcinoma

# This script just samples RNA from the link above. it should be able to intepret other sets of data from the site.
# ideally this will be a command line tool... so that means
# doing something with this: http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
####################################

#####################################
##		 INSTRUCTIONS FOR USE:		#
#####################################
## py file must be in same folder as the topmost layer of the gene sequence folder.
## go to Tools > Build, or press cmd + B to run the script.

##############################
# SETTING UP DATA STRUCTURE  #
##############################

# this is a library used to read files in
import csv

# we will fill this Cabinet array with objects of class TissueSample..
# each index (like cabinet[0] or cabinet[1]) will have an object. See the class TissueSample below..
cabinet = [] # array will hold TissueSample objects, holding a tissue sample and it's data.
samples = [] # array will hold just sample names to verify the cabinet.

# file path's are relative to where the py script is saved. so they could cause problems if you aren't lookin the right place.
manifestFile = "TCGA CHOL RNA-seq/file_manifest.txt"; #this is the manifest file path. it has sample names and filenames.

#append this before each barcode filename so python can find the file.
pathToDataFiles = "TCGA CHOL RNA-seq/RNASeqV2/UNC__IlluminaHiSeq_RNASeqV2/Level_3/"

# This is a class definition, an object called TissueSample that will hold all information for the sample.
class TissueSample:
	def __init__(self,sample): # function initializes class, must pass in a sample and tissue type.
		self.sample = sample;				#see example below class definition
	#attributes for the TissueSample. These hold the filenames for data, and will hold data themselves.
	genes_results = {"gene_id":"multiple_transcript_ids", #attribute variable with dictionary
					"filename": ""}
	genes_norms = {"gene_id":"normalized_count",
					"filename": ""}
	isoforms_norms = {"isoform_id":"normalized_count",
					"filename": ""}
	tissue_type = "none";
	def add_tissue_type(self,tt):
		self.tissue_type = tt;
	def add_isoforms_norms(self,isoforms_norms_file): #functions to add attribute to the object...
		path = pathToDataFiles + "/" + isoforms_norms_file;# filename passed from manifest needs it's path prepended.
		self.isoforms_norms['filename'] = path; 			# so we use functions for the name, but when adding genes
		with open(path, 'rb') as f:
			print "\t\tReading in Isoforms Normalized Results and storing in TissueSample in cabinet."
			reader = csv.reader(f, delimiter="\t")
			for line in reader:
				self.isoforms_norms[line[0]] = line[1]

	def add_genes_norms(self,genes_norms_file):
		path = pathToDataFiles + "/" + genes_norms_file;
		self.genes_norms['filename'] = path;
		with open(path, 'rb') as f:
			print "\t\tReading in Genes Normalized Results and storing in TissueSample."
			reader = csv.reader(f, delimiter="\t")
			for line in reader:
				self.genes_norms[line[0]] = line[1]

	def add_genes_results(self,genes_results_file):
		path = pathToDataFiles + "/" + genes_results_file;
		self.genes_results['filename'] = path;
		with open(path, 'rb') as f:
			print "\t\tReading in Gene Results and adding to TissueSample in cabinet"
			reader = csv.reader(f, delimiter="\t")
			for line in reader:
				arrayify = line[3].split(",")
				self.genes_results[line[0]] = arrayify;
# you can add attributes (or attr's) to your cases by defining (or def) functions to input
# learned from: http://sthurlow.com/python/lesson08/

#############################
#Reading in the file_manifest
#############################

fileInCabinet = False; #this boolean is to let us know if we found the sample name in the cabinet.
placeHolder = -1; #if the sample is in the cabinet, then this number will be it's index.
i = 0;

with open(manifestFile, 'rb') as f:
	reader = csv.reader(f, delimiter="\t")
	print "Reading in file_manifest, line by line..."
	for line in reader:
		i = i+1
		if "rsem" in line[6]:#remove top 3 rows, and also two quantification filename_barcodes per sample b/c unnecessary
			print "\nLine", i,"from manifest. Sample:", line[5], "\n\t\tBarcode_filename: ",line[6].split("rsem.",1)[1]

			for l in cabinet: #search the cabinet for this key
				if (line[5] == l.sample): #the sample is already in cabinet.
					print "\t\tFound the TissueSample in cabinet! placeHolder: ", placeHolder
					fileInCabinet = True; #change boolean for flow control.s
					placeHolder = cabinet.index(l); #find position of the TissueSample

			if (fileInCabinet == True): #this needs to be after the for loop searching cabinet.
										#b/c we search the whole cabinet for the file.
				if "genes.normalized" in line[6]:
					cabinet[placeHolder].add_genes_norms(line[6])

				elif "genes.results" in line[6]:
					cabinet[placeHolder].add_genes_results(line[6]);

				elif "isoforms.normalized" in line[6]:
					cabinet[placeHolder].add_isoforms_norms(line[6]);

				else:
					print "\t\tthe associated barcode_filename is not needed"
				fileInCabinet = False #now search is done, reset this indicator for next sample.
			else: #the sample is not in Cabinet.
				x = TissueSample(line[5]) #We make an new instance of the object

				print "\t\tTissueSample is not in cabinet. Adding new case with sample", x.sample
				if "genes.normalized" in line[6]:
					x.add_genes_norms(line[6])

				elif "genes.results" in line[6]:
					x.add_genes_results(line[6])

				elif "isoforms.normalized" in line[6]:
					x.add_isoforms_norms(line[6])

				cabinet.append(x) #and add it to the cabinet.
		else: #this means the string "rsem." is not in line[6], therefore the line isn't important for our purposes.
			print "\nLine",i,"does not contain a sample or proper barcode_filename\n"

#reading in tissuetype. THIS DOESNT WORK YET.
tissue_type_file = "tcga CHOL sample bar code_tissuetype.csv"

with open(tissue_type_file, 'rb') as f:
	reader = csv.reader(f, delimiter=",")

	print "Reading in tissue type, line by line..."
	currCase = 'n/a';
	tissue = 'n/a';
	for line in reader:
		print 'line0:',line[0],'line1', line[1]
		if (line[0].strip() == 0):
			currCase = line[1]
			print 'current TissueSample:',currCase
		else:
			for thing in cabinet:
				if (thing.sample == currCase):
					thing.add_tissue_type(line[1])
					print 'added tissue tupe to TissueSample'



#Printing the cabinet to console!
print "\n\nOverview of Filing Cabinet w/ shortened filenames..."
print '-' * 55
for l in cabinet:
	print "\tcase:",cabinet.index(l),l.sample, l.genes_results['filename'].split("rsem.",1)[1], l.genes_norms['filename'].split("rsem.",1)[1], l.isoforms_norms['filename'].split("rsem.",1)[1], '\n'
print "Overview of Filing Cabinet w/ shortened filenames printed above."
print '--length of cabinet: ', len(cabinet)

#Testing one object for its gene_id data.
print "\n\ntesting a single object for its data."
currCase = cabinet[0];
print "currCase: ", currCase.sample, "tissue_type:", currCase.tissue_type
print "Displaying gene_id's and their normalized_counts for this sample."
for key, val in currCase.genes_norms.iteritems():
	print "gene_id:",key, "normalized_count:",val, "sample:",currCase.sample, "tissue_type:",currCase.tissue_type

# instead of storing those values in python,
# i want to output them into files that he can read with R or Perl...
#one file for each sample?
