# This script will read the results of sequenced samples of CCA. MUST BE ORGANIZED AND STAT ANALYZED
# see this url to retreive sequencing data: https://tcga-data.nci.nih.gov/tcga/tcgaCancerDetails.jsp?diseaseType=CHOL&diseaseName=Cholangiocarcinoma
# There are two different types... RNA and Micro-RNA
# This script just samples RNA...

#This script is personalized to the specific data my brother wanted. But ideally this will be a command line tool... so that means
# doing something like this: http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html

# this is a library used to read files in
import csv

# cabinet is an array. we will populate with objects of class Case..
# each index (like cabinet[0] or cabinet[1]) is an object you can explore
# with something like cabinet[9].barcode or cabinet[]
cabinet = []
numberOfCases = 36 + 9 #36 matched cases plus 9 healthy cases.
samples = []

#these arrays are to store user input, it is a step towards making this code reproducable for any dataset of sequenced genomes.
samplesYouNeed = [];
barcodeFilenamesYouNeed = [];


#this is the overall structure of each case. There will be 45 total for the RNA
class Case:
	def __init__(self,sample,tissue_type):
		self.sample = sample;
		self.tissue_type = tissue_type;
		#self.files
	genes_results = ""
	isoforms_results = ""
	genes_norms = ""
	isoforms_norms = ""
	def add_isoforms_norms(self,isoforms_norms): #function to add attribute to the object...
		self.isoforms_norms = isoforms_norms;
	def add_genes_norms(self,genes_norms):
		self.genes_norms = genes_norms;
	def add_genes_results(self,genes_results):
		self.genes_results = genes_results;
	def add_isoforms_results(self,isoforms_results):
		self.isoforms_results = isoforms_results;
# you can add attributes (or attr's) to your cases by defining (or def) functions to input
# check out the code i already wrote and mess figure out how it works...
# learned from: http://sthurlow.com/python/lesson08/


###### sample of initiating the cases...
#for num in range(0, numberOfCases):
#	x = Case("sample","tissue_type")
#	cabinet.append(x)
##### you can use "Case.attr(...)" to make attributes for your case...

samples = [];
samplesLinkedToFiles = {};
fileInCabinet = False;
placeHolder = -1;

# reading in the RNA file_manifest
i = 0;
with open('TCGA CHOL RNA-seq/file_manifest.txt', 'rb') as f:
	reader = csv.reader(f, delimiter="\t")
	print "reading in file_manifest, line by line..."
	for line in reader:
		i = i+1
		if "rsem" in line[6]:#removed the top three rows of manifest & two quantification filename_barcodes b/c unnecessary
			print "\nLine", i,"from manifest. Sample:", line[5], "Barcode_filename: ",line[6]#.split("rsem.",1)[1] #not necessary
			samples.append(line[5]) #not necassary but shines a light on sample names
			print "		searching cabinet...\nCurrent state of Cabinet:"
			for l in cabinet:
				print l.sample
				if (l.genes_results):
					print "\t\t\t\t\t\t\t", l.genes_results.split("rsem.",1)[1], "[check!]"
				if (l.genes_norms):
					print "\t\t\t\t\t\t\t", l.genes_norms.split("rsem.",1)[1], "[check!]"
				if (l.isoforms_norms):
					print "\t\t\t\t\t\t\t",l.isoforms_norms.split("rsem.",1)[1], "[check!]"
				if (l.isoforms_results):
					print "\t\t\t\t\t\t\t",l.isoforms_results.split("rsem.",1)[1], "[check!]"
				if (line[5] == l.sample): #the sample is already in cabinet
					fileInCabinet = True;
					placeHolder = cabinet.index(l); #find position of the Case
					print "		Found the case in cabinet"
					print "		placeHolder: ", placeHolder, "for case in cabinet"
			if (fileInCabinet == True): #this needs to be after the for loop
										#b/c we search the whole cabinet
				if "genes.normalized" in line[6]:
					cabinet[placeHolder].add_genes_norms(line[6])
					print "\t\tGenes_norms added to case in cabinet"
				elif "genes.results" in line[6]:
					cabinet[placeHolder].add_genes_results(line[6])
					print "\t\tgenes_results added to case in cabinet"
				elif "isoforms.normalized" in line[6]:
					cabinet[placeHolder].add_isoforms_norms(line[6])
					print "\t\tisoforms_norms added to case in cabinet"
				elif "isoforms.results" in line[6]:
					cabinet[placeHolder].add_isoforms_results(line[6])
					print "\t\tgenes_results added to case in cabinet"
				else:
					print "\t\tthe associated barcode_filename is not needed"
				fileInCabinet = False #now search is done, reset this indicator for next sample name
			else: #the sample is not already in Cabinet... (fileInCabinet == false)
				print "\t\tthe case wasn't found in cabinet"
				x = Case(line[5], 'none')
				print "\t\tcase with sample", x.sample, "added to filing cabinet"
				if "genes.normalized" in line[6]:
					x.add_genes_norms(line[6])
					print "\t\twith genes_norms", x.sample
				elif "genes.results" in line[6]:
					x.add_genes_results(line[6])
					print "\t\twith genes_results", x.sample
				elif "isoforms.results" in line[6]:
					x.add_isoforms_results(line[6])
					print "\t\twith isoforms_results", x.sample
				elif "isoforms.normalized" in line[6]:
					x.add_isoforms_norms(line[6])
					print "\t\twith isoforms_norms", x.sample
				cabinet.append(x)
		else:
			print "current row",i,"does not contain a sample or proper barcode_filename\n"
			#cabinet.append(x)

setSamples = list(set(samples))

print "set of all sample names: ", len(samples), "set of unique of sample names: ", len(setSamples)
for l in setSamples:
	print "unique sample name: ", l

print "final state of filing Cabinet w/ shortened filenames..."
for l in cabinet:
	print l.sample, l.genes_results.split("rsem.",1)[1], l.genes_norms.split("rsem.",1)[1], l.isoforms_norms.split("rsem.",1)[1], l.isoforms_results.split("rsem.",1)[1], '\n'
print 'length of cabinet: ', len(cabinet)

print "verify that all samples are in the cabinet..."
for l in setSamples:
	print cabinet.index(l)

print cabinetCount

# once i get all of the proper files into the proper gene Case, i can move to read in those files and extract
# the results Larry needs for his research
# instead of storing those values in python, i want to output them into files that he can read with R or Perl...
