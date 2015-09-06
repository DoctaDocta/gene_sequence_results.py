
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

# we will fill this Cabinet array with objects of class Case..
# each index (like cabinet[0] or cabinet[1]) will have an object. See the class Case below..
cabinet = [] # array will hold case objects, holding a tissue sample and it's data.
samples = [] # array will hold just sample names to verify the cabinet.

# file path's are relative to where the py script is saved. so they could cause problems if you aren't lookin the right place.
manifestFile = "TCGA CHOL RNA-seq/file_manifest.txt"; #this is the manifest file path. it has sample names and filenames.

#append this before each barcode filename so python can find the file.
pathToDataFiles = "TCGA CHOL RNA-seq/RNASeqV2/UNC__IlluminaHiSeq_RNASeqV2/Level_3/"

# This is a class definition, an object called Case that will hold all information for the sample.
class Case:
	def __init__(self,sample,tissue_type): # function initializes class, must pass in a sample and tissue type.
		self.sample = sample;				#see example below class definition
		self.tissue_type = tissue_type;
	#attributes for the Case. These hold the filenames for data, and will hold data themselves.
	genes_results = {"gene_id":"multiple_transcript_ids", #attribute variable with dictionary
					"filename": ""}
	genes_norms = {"gene_id":"normalized_count",
					"filename": ""}
	isoforms_norms = {"isoform_id":"normalized_count",
					"filename": ""}
	def add_isoforms_norms_file(self,isoforms_norms_file): #functions to add attribute to the object...
		path = pathToDataFiles + "/" + isoforms_norms_file;# filename passed from manifest needs it's path prepended.
		self.isoforms_norms['filename'] = path; 			# so we use functions for the name, but when adding genes
															#we'll do it like this  genes_norms['gene_id'] = line[1].
	def add_genes_norms_file(self,genes_norms_file):
		path = pathToDataFiles + "/" + genes_norms_file;
		self.genes_norms['filename'] = path;

	def add_genes_results_file(self,genes_results_file):
		path = pathToDataFiles + "/" + genes_results_file;
		self.genes_results['filename'] = path;
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
			samples.append(line[5]) #not necassary, collects sample names for comparison to cabinet.
			#print "\t\tCurrent state of Cabinet:"
			for l in cabinet:
				'''
				print l.sample
				if (l.genes_results['filename']):
					print "\t\t\t\t\t\t\t", l.genes_results['filename'].split("rsem.",1)[1], "[check!]" #split breaks one string into two from the end of the keyword it is passed.
				if (l.genes_norms['filename']):															#and the end [1] picks the string after the keyword, not the string before.
					print "\t\t\t\t\t\t\t", l.genes_norms['filename'].split("rsem.",1)[1], "[check!]"	# I did this jsut for readability. We need the whole filename stored in the Case.
				if (l.isoforms_norms['filename']):
					print "\t\t\t\t\t\t\t",l.isoforms_norms['filename'].split("rsem.",1)[1], "[check!]"
				'''
				if (line[5] == l.sample): #the sample is already in cabinet.
					fileInCabinet = True; #change boolean for flow control.s
					placeHolder = cabinet.index(l); #find position of the Case
					print "		Found the case in cabinet"
					print "		placeHolder: ", placeHolder, "for case in cabinet"
			if (fileInCabinet == True): #this needs to be after the for loop searching cabinet.
										#b/c we search the whole cabinet for the file.
				if "genes.normalized" in line[6]:
					cabinet[placeHolder].add_genes_norms_file(line[6])
					filePath = cabinet[placeHolder].genes_norms['filename']
					with open(filePath, 'rb') as f:
						print "\n\nReading in Gene Normalized Results and storing in case."
						reader = csv.reader(f, delimiter="\t")
						for line in reader:
							cabinet[placeHolder].genes_norms[line[0]] = line[1]
					print "\t\tGenes_norms added to case in cabinet"

				elif "genes.results" in line[6]:
					cabinet[placeHolder].add_genes_results_file(line[6]);
					filePath = cabinet[placeHolder].genes_results['filename']
					with open(filePath, 'rb') as f:
						print "\n\nReading in Gene Results"
						reader = csv.reader(f, delimiter="\t")
						for line in reader:
							arrayify = line[3].split(",")
							cabinet[placeHolder].genes_results[line[0]] = arrayify;
					print "\t\tgenes_results['filename'] added to case in cabinet"

				elif "isoforms.normalized" in line[6]:
					cabinet[placeHolder].add_isoforms_norms_file(line[6]);
					filePath = cabinet[placeHolder].isoforms_norms['filename']
					with open(filePath, 'rb') as f:
						print "\n\nReading in Isoforms Normalized Results and storing in case."
						reader = csv.reader(f, delimiter="\t")
						for line in reader:
							cabinet[placeHolder].isoforms_norms[line[0]] = line[1]
					print "\t\tisoforms_norms added to case in cabinet"
				else:
					print "\t\tthe associated barcode_filename is not needed"
				fileInCabinet = False #now search is done, reset this indicator for next sample.
			else: #the sample is not in Cabinet.
				print "\t\tthe case wasn't found in cabinet"
				x = Case(line[5], 'none') #We must make an object
				print "\t\tcase with sample", x.sample, "added to filing cabinet"
				if "genes.normalized" in line[6]:
					x.add_genes_norms_file(line[6])
					filePath = x.genes_norms['filename']
					with open(filePath, 'rb') as f:
						print "\n\nReading in Gene Normalized Results and storing in case."
						reader = csv.reader(f, delimiter="\t")
						for line in reader:
							x.genes_norms[line[0]] = line[1] # give the object an attribute
					print "\t\twith genes_norms['']", x.sample
				elif "genes.results" in line[6]:
					x.add_genes_results_file(line[6])
					filePath = x.genes_results['filename']
					with open(filePath, 'rb') as f:
						print "\n\nReading in Gene Results"
						reader = csv.reader(f, delimiter="\t")
						for line in reader:
							arrayify = line[3].split(",")
							x.genes_results[line[0]] = arrayify;
					print "\t\twith genes_results['filename']", x.sample
				elif "isoforms.normalized" in line[6]:
					x.add_isoforms_norms_file(line[6])
					filePath = x.isoforms_norms['filename']
					with open(filePath, 'rb') as f:
						print "\n\nReading in Isoforms Normalized Results and storing in case."
						reader = csv.reader(f, delimiter="\t")
						for line in reader:
							x.isoforms_norms[line[0]] = line[1]
					print "\t\twith isoforms_norms_file", x.sample
				cabinet.append(x) #and add it to the cabinet.
		else: #this means the string "rsem." is not in line[6], therefore the line isn't important for our purposes.
			print "current row",i,"does not contain a sample or proper barcode_filename\n"



#This part is concerned with checking the manifest readin, and printing to console for you
setSamples = list(set(samples)) #eliminate redundant sample names, since each sample should have appeared 4 times.
cabinetSampleNames = []#array to compare to setSamples for verifying that we caught all samples.

#Printing the cabinet to console!
print "\n\nOverview of Filing Cabinet w/ shortened filenames..."
print '-' * 55
for l in cabinet:
	cabinetSampleNames.append(l.sample) #fill the verification array
	print "\tcase:",cabinet.index(l),l.sample, l.genes_results['filename'].split("rsem.",1)[1], l.genes_norms['filename'].split("rsem.",1)[1], l.isoforms_norms['filename'].split("rsem.",1)[1], '\n'
print "Overview of Filing Cabinet w/ shortened filenames printed above."
print '--length of cabinet: ', len(cabinet)


diffCheck = (set(cabinetSampleNames) - set(setSamples)); #array with only uncommon elements.
if diffCheck: #if diffCheck is an array that is NOT empty
	print "**verification failed! The cabinet is missing something."
	for l in diffCheck:
		print l
else: # else, diffCheck is empty array
	print "--verfication complete! The cabinet is up to date."

print "\ttesting a single object for its data."
currCase = cabinet[0];
print "currCase: ", currCase.sample, "tissue_type:", currCase.tissue_type
print "Displaying gene_id's and their normalized_counts for this sample."
for key, val in currCase.genes_norms.iteritems():
	print "gene_id:",key, "normalized_count:",val, "sample:",currCase.sample, "tissue_type:",currCase.tissue_type


# Now all the associated files for each sample are in the same Case, all in the array called Cabinets

# i need to go into each file for the results Larry needs for his research
# instead of storing those values in python,
# i want to output them into files that he can read with R or Perl...
