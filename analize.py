######## README
# This script will read the results of sequenced samples of CCA. MUST BE ORGANIZED AND STAT ANALYZED
# see this url to retreive sequencing data: https://tcga-data.nci.nih.gov/tcga/tcgaCancerDetails.jsp?diseaseType=CHOL&diseaseName=Cholangiocarcinoma
# This script just samples RNA...
#This script is personalized to the specific data my brother wanted. But ideally this will be a command line tool... so that means
# doing something with this: http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html
########

######## INSTRUCTIONS FOR USE:
## File must be in same folder as data, at the topmost layer.
## go to Tools > Build, or press cmd + B to run the script.
########

# this is a library used to read files in
import csv

# cabinet is an array. we will populate with objects of class Case..
# each index (like cabinet[0] or cabinet[1]) is an object you can explore
# with something like cabinet[9].barcode or cabinet[]
cabinet = [] #this array will hold 45 object containing info on each sample.
numberOfCases = 36 + 9 #36 matched cases plus 9 healthy cases.
samples = [] #this array will hold sample names to verify the cabinet.


manifestFile = "TCGA CHOL RNA-seq/file_manifest.txt"; #this is the manifest.
#append this before each filename so python can find the file.
# it is based on folder structure of results dl'd from website.
pathToDataFiles = "TCGA CHOL RNA-seq/RNASeqV2/UNC__IlluminaHiSeq_RNASeqV2/Level_3/"

# these arrays are to store user input
# a step towards making this code reproducable for any set of sequenced gene results.
# the idea being that the code will seek out those n
samplesYouNeed = [];
barcodeFilenamesYouNeed = []; #for each sample. this way you can easily filter by comparing incoming files to this array
specificResults = []; #what actual numbers do you want? its the data within the barcode filenames that you want to see.

#should this just be a json object?
# This is a class definition, an object called Case that will hold all information for the sample.
class Case:
	def __init__(self,sample,tissue_type): # function initializes class, must pass in a sample and tissue type.
		self.sample = sample;				#see example below class definition
		self.tissue_type = tissue_type;
		#self.files
	genes_results_file = ""; #attributes for the Case. These are filenames. We also need specific data names.
	genes_results = {"geneId":"multiple transcript id's"}
	isoforms_results_file = "";
	isoforms_results = {"isoform_id":"scaled_estimate??"}
	genes_norms_file = "";
	genes_norms = {"gene_id":"normalized_count"}
	isoforms_norms_file = "";
	def add_isoforms_norms_file(self,isoforms_norms_file): #functions to add attribute to the object...
		self.isoforms_norms_file = isoforms_norms_file;
		path = pathToDataFiles + "/" + isoforms_norms_file;

	def add_genes_norms(self,genes_norms_file):
		self.genes_norms_file = genes_norms_file;
		path = pathToDataFiles + "/" +  genes_norms_file;

	def add_genes_results_file(self,genes_results_file):
		self.genes_results_file = genes_results_file;
		path = pathToDataFiles + "/" + genes_results_file;

	def add_isoforms_results(self,isoforms_results_file):
		self.isoforms_results_file = isoforms_results_file;
		path = pathToDataFiles + "/" +  isoforms_results_file;

# you can add attributes (or attr's) to your cases by defining (or def) functions to input
# check out the code i already wrote and mess figure out how it works...
# learned from: http://sthurlow.com/python/lesson08/


###### sample of initiating the cases... A very basic example###############
#for num in range(0, numberOfCases):									   #
#	x = Case("sample","tissue_type")								   	   #
#	cabinet.append(x)													   #
##### you can use "Case.attr(...)" to make attributes for your case...######




#Reading in the RNA file_manifest

fileInCabinet = False; #this boolean is to let us know if we found the sample name in the cabinet.
placeHolder = -1; #if the sample is in the cabinet, then this number will be it's index.

i = 0;
with open(manifestFile, 'rb') as f:
	reader = csv.reader(f, delimiter="\t")
	print "Reading in file_manifest, line by line..."
	for line in reader:
		i = i+1
		if "rsem" in line[6]:#remove top 3 rows, and also two quantification filename_barcodes per sample b/c unnecessary
			print "\nLine", i,"from manifest. Sample:", line[5], "\nBarcode_filename: ",line[6].split("rsem.",1)[1] #not necessary
			samples.append(line[5]) #not necassary, collects sample names for comparison to cabinet.
			print "\t\tCurrent state of Cabinet:"
			for l in cabinet:
				print l.sample
				if (l.genes_results_file):
					print "\t\t\t\t\t\t\t", l.genes_results_file.split("rsem.",1)[1], "[check!]" #split breaks one string into two from the end of the keyword it is passed.
				if (l.genes_norms_file):															#and the end [1] picks the string after the keyword, not the string before.
					print "\t\t\t\t\t\t\t", l.genes_norms_file.split("rsem.",1)[1], "[check!]"	# I did this jsut for readability. We need the whole filename stored in the Case.
				if (l.isoforms_norms_file):
					print "\t\t\t\t\t\t\t",l.isoforms_norms_file.split("rsem.",1)[1], "[check!]"
				if (l.isoforms_results_file):
					print "\t\t\t\t\t\t\t",l.isoforms_results_file.split("rsem.",1)[1], "[check!]"
				if (line[5] == l.sample): #the sample is already in cabinet.
					fileInCabinet = True; #change boolean for flow control.s
					placeHolder = cabinet.index(l); #find position of the Case
					print "		Found the case in cabinet"
					print "		placeHolder: ", placeHolder, "for case in cabinet"
			if (fileInCabinet == True): #this needs to be after the for loop
										#b/c we search the whole cabinet for the file.
				if "genes.normalized" in line[6]:
					cabinet[placeHolder].add_genes_norms(line[6])
					print "\t\tGenes_norms added to case in cabinet"
				elif "genes.results" in line[6]:
					cabinet[placeHolder].add_genes_results_file(line[6])
					print "\t\tgenes_results_file added to case in cabinet"
				elif "isoforms.normalized" in line[6]:
					cabinet[placeHolder].add_isoforms_norms_file(line[6])
					print "\t\tisoforms_norms_file added to case in cabinet"
				elif "isoforms.results" in line[6]:
					cabinet[placeHolder].add_isoforms_results(line[6])
					print "\t\tgenes_results_file added to case in cabinet"
				else:
					print "\t\tthe associated barcode_filename is not needed"
				fileInCabinet = False #now search is done, reset this indicator to False for next sample.
			else: #the sample is not in Cabinet.
				print "\t\tthe case wasn't found in cabinet"
				x = Case(line[5], 'none') #We must make an object
				print "\t\tcase with sample", x.sample, "added to filing cabinet"
				if "genes.normalized" in line[6]:
					x.add_genes_norms(line[6]) # give the object an attribute
					print "\t\twith genes_norms_file", x.sample
				elif "genes.results" in line[6]:
					x.add_genes_results_file(line[6])
					print "\t\twith genes_results_file", x.sample
				elif "isoforms.results" in line[6]:
					x.add_isoforms_results(line[6])
					print "\t\twith isoforms_results_file", x.sample
				elif "isoforms.normalized" in line[6]:
					x.add_isoforms_norms_file(line[6])
					print "\t\twith isoforms_norms_file", x.sample
				cabinet.append(x) #and add it to the cabinet.
		else: #this means the string "rsem." is not in line[6], therefore the line isn't important for our purposes.
			print "current row",i,"does not contain a sample or proper barcode_filename\n"

#This part is concerned with checking the manifest readin, and printing to console for you
setSamples = list(set(samples)) #eliminate redundant sample names, since each sample should have appeared 4 times.
print "set of unique of sample names: ", len(setSamples)
for l in setSamples:
	print "\tsample name: ", l #this prints to log.


cabinetSampleNames = []#array to compare to setSamples for verifying that we caught all samples.

print "\n\nOverview of Filing Cabinet w/ shortened filenames..."
for l in cabinet:
	cabinetSampleNames.append(l.sample) #fill the verification array
	print "\t",cabinet.index(l),l.sample, l.genes_results_file.split("rsem.",1)[1], l.genes_norms_file.split("rsem.",1)[1], l.isoforms_norms_file.split("rsem.",1)[1], l.isoforms_results_file.split("rsem.",1)[1], '\n'
print 'length of cabinet: ', len(cabinet)

diffCheck = (set(cabinetSampleNames) - set(setSamples)); #array with only uncommon elements.
if diffCheck: #if diffCheck is an array that is NOT empty
	print "verification failed! The cabinet is missing something."
	for l in diffCheck:
		print l
else: # else, diffCheck is empty array
	print "verfication complete! The cabinet is up to date."

# Now all the associated files for each sample are in the same Case, all in the array called Cabinets

# i need to go into each file for the results Larry needs for his research
# instead of storing those values in python,
# i want to output them into files that he can read with R or Perl...

#test import of gene_results
filePath = pathToDataFiles + cabinet[0].genes_results_file
with open(filePath, 'rb') as f:
	reader = csv.reader(f, delimiter="\t")
	for line in reader:
		print line
		arrayify = line[3].split(",")
		lengthArrayify = len(arrayify)
		cabinet[0].genes_results[line[0]] = arrayify
		for l in arrayify:
			print l
ctr = 0;
while ctr<10:
	for l, m in cabinet[0].genes_results:
		print l, m
		ctr = ctr + 1
