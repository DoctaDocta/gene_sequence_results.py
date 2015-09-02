# This script will read the results of sequenced samples of CCA. MUST BE ORGANIZED AND STAT ANALYZED
# see this url to retreive sequencing data: ________________________
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

#this is the overall structure of each case. There will be 45 total for the RNA
class Case:
	def __init__(self,sample,tissue_type):
		self.sample = sample;
		self.tissue_type = tissue_type;
		#self.files
	genes_results = "nothing added yet..."
	isoforms_results = "nothing added yet..."
	genes_norms = "..."
	isoforms_norms = "..."
	def isoforms_norms(self,isoforms_norms):
		self.isoforms_norms = isoforms_norms;
	def genes_norms(self,genes_norms):
		self.genes_norms = genes_norms;
	def genes_results(self,genes_results):
		self.genes_results = genes_results;
	def isoforms_results(self,isoforms_results):
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

# reading in the RNA file_manifest
i = 0;
with open('TCGA CHOL RNA-seq/file_manifest.txt', 'rb') as f:
	reader = csv.reader(f, delimiter="\t")
	for line in reader:
		i = i+1
		if "TCGA" in line[5]:
			samples.append(line[5]) #not necassary
			for l in cabinet:
				print "current case: ", l.sample
				if (line[5] != l.sample):
					x = Case(line[5], 'none')
					if "genes.normalized" in line[6]:
						x.genes_norms(line[6])
					elif "genes.results" in line[6]:
						x.genes_results(line[6])
					elif "isoforms.results" in line[6]:
						x.isoforms_results(line[6])
					elif "isoforms.normalized" in line[6]:
						x.isoforms_norms(line[6])
					cabinet.append(x)
				else:
					placeHolder = cabinet.index(line[5])
					print "placeHolder: ", placeHolder
					if "genes.normalized" in line[6]:
						cabinet[placeHolder].genes_norms(line[6])
					if "genes.results" in line[6]:
						cabinet[placeHolder].genes_results(line[6])
					if "isoforms.normalized" in line[6]:
						cabinet[placeHolder].genes_norms(line[6])
					if "isoforms.results" in line[6]:
						cabinet[placeHolder].genes_norms(line[6])
		#cabinet.append(x)
		print "sample: ", line[5], "barcode_filename: ",line[6] #not necessary


print "whole list of samples: ", len(samples), "verified by lines in RNA manifest: ", i/6
setSamples = list(set(samples))
for l in setSamples:
	print "sample in array 'samples': ", l
print "simplified list of samples: ", len(setSamples)
