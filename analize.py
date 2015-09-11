
#####################################
#		 ABOUT THIS SCRIPY 			#
#####################################
# This script will read the results of sequenced barcodes of tissue
# so they can easily be searched and organized by the scientist.
# URL to retreive gene sequencing data for CCA tissue: https://tcga-data.nci.nih.gov/tcga/tcgaCancerDetails.jsp?diseaseType=CHOL&diseaseName=Cholangiocarcinoma

#####################################
##		 INSTRUCTIONS FOR USE:		#
#####################################
## py file must be in same folder as the topmost layer of the gene sequence folder.
## go to Tools > Build, or press cmd + B to run the script.

# This script just barcodes RNA from the link above. it should be able to intepret other sets of data from the site.
# ideally this will be a command line tool... http://www.diveintopython.net/scripts_and_streams/command_line_arguments.html

#####################################
# SETTING UP DATA STRUCTURE  		#
#####################################
# this is a library used to read files in
import csv
# these libraries will help us write our info to a database. easiest to read in.
import sqlite3 as lite
import sys
#setting up the outfile for out results!
con = lite.connect('geneSequenceResults.db'); #initilazing output file
cur = con.cursor() #save cursor to var
cur.execute("DROP TABLE IF EXISTS genes") #if this table doesn't exist, create it.
cur.execute("CREATE TABLE genes (id text, count real, barcode text, tissue text)")#vals in each col of table


# we will fill this Cabinet list with objects of class TissueSample..
cabinet = [] # array will hold TissueSample objects, holding a tissue barcode and it's data.

# file path's are relative to where the py script is saved. so they could cause problems if you aren't lookin the right place.
manifestFile = "TCGA CHOL RNA-seq/file_manifest.txt"; #this is the manifest file path. it has barcode names and filenames.
#append this before each barcode filename so python can find the file.
pathToDataFiles = "TCGA CHOL RNA-seq/RNASeqV2/UNC__IlluminaHiSeq_RNASeqV2/Level_3/"; # where the files are the scientist wants.
filenameKeywords = ["genes.results","genes.normalized","isoforms.normalized"]; # the files scientist wants for his study.
tissue_type_file = "tcga CHOL sample bar code_tissuetype.csv"; #file made by scientist.


########################################################
#Reading Samples: Tissue Types. Adding to dictionary.###
########################################################
tissueTypeDict = {}; #this will be the reference for when we find a sample further down.
currCase = 'empty'; #helper variables for reading tissue type.
tissue = 'empty';
with open(tissue_type_file, 'rb') as f:
	reader = csv.reader(f, delimiter=",")
	print "\n\nReading in tissue type, line by line..."
	#print "current case:", currCase, "current tissue:", tissue
	ctr = 0;
	for line in reader:
		if (int(line[0]) == 0): #int() converts string to integer
			currCase = line[1]
		else:
			tissue = line[1]
			tissueTypeDict[currCase] = tissue;
			currCase = 'reset'
			tissue = "reset"
		ctr = ctr + 1;
	print "Done!"


tmpList = []; #just preloading. this will be used to populate the db file! see the class

# This is a class definition, an object called TissueSample that will hold all information for the barcode.
class TissueSample:
	def __init__(self,barcode): # function initializes class, must pass in a barcode and tissue type.
		self.barcode = barcode;				#see example below class definition
		self.sample = barcode[:15] #the sample is first 15 char, see manifest for example.
		self.tissue_type = tissueTypeDict[self.sample]; #find matching tissue type.
		print "\t\tFound tissue type:", self.barcode, self.tissue_type, "Added to cabinet!"
	#attributes for the TissueSample. These hold the filenames for data, and will hold data themselves.
	genes_results = {"gene_id":"multiple_transcript_ids", #attribute  with dictionary
					"filename": ""} #currently set at NULL, and genes_results['filename'] is considered NULL.
	genes_norms = 	{"gene_id":"normalized_count",
					"filename": ""}
	isoforms_norms = {"isoform_id":"normalized_count", #isoform_id == transcript id from gene.results
						"filename": ""}
	tissue_type = "none";

# you can add attributes (or attr's) to your cases by defining (or def) functions to input
# learned from: http://sthurlow.com/python/lesson08/

	'''def add_isoforms_ids(self):
		with open(self.genes_results['filename'], 'rb') as f: #use the file we read in to get all its necessary contents
				print "\t\tReading in corresponding Genes and Isoforms IDs, and each iso_id normcount. Writing to Database."
				reader = csv.reader(f, delimiter="\t")
				for line in reader:
					arrayify = line[3].split(",") #arrafiy is a list of transcript ids. they match to isoforms norms file.
					self.genes_results[line[0]] = arrayify;
	'''
	def add_isoforms_norms(self,isoforms_norms_file): #functions to add attribute to the object...
		path = pathToDataFiles + isoforms_norms_file;# filename passed from manifest needs it's path prepended.
		self.isoforms_norms['filename'] = path; 			# so we use functions for the name, but when adding genes
		print "\t\tAdded filename, but not actual data for this script version."
		'''if (self.genes_results['filename']):
			with open(path, 'rb') as f: #use the file we read in to get all its necessary contents
				print "\t\tReading in Isoforms Normalized Results and storing in TissueSample in cabinet."
				reader = csv.reader(f, delimiter="\t")
				for line in reader:
					self.isoforms_norms[line[0]] = line[1] #add this data to the dict attribute above
		'''
	def add_genes_norms(self,genes_norms_file):
		path = pathToDataFiles + genes_norms_file;
		self.genes_norms['filename'] = path;
		with open(path, 'rb') as f:
			print "\t\tReading in Genes Normalized Results and executing to DB."
			reader = csv.reader(f, delimiter="\t")
			tmpList = [];
			for line in reader:
				tmpList = [];
				#self.genes_norms[line[0]] = line[1]
				tmpList.extend([line[0],line[1],self.barcode,self.tissue_type]);
				#print tmpList
				cur.execute('INSERT INTO genes VALUES (?,?,?,?)', tmpList)
				#con.commit()
		#cur.execute("SELECT * FROM genes")
		#rows = cur.fetchall()
		#for row in rows:
		#	print row
		#this is where we will export our fulfilled TissueSample object to a table using sqlite.

	def add_genes_results(self,genes_results_file):
		path = pathToDataFiles + genes_results_file;
		self.genes_results['filename'] = path;
		print "\t\tAdded filename, but not actual data for this script version."

		'''with open(path, 'rb') as f:
			print "\t\tReading in Gene Results and adding to TissueSample in cabinet"
			reader = csv.reader(f, delimiter="\t")
			if (self.isoforms_norms['filename']):
				for line in reader:
					arrayify = line[3].split(",") #arrafiy is a list of transcript ids. they match to isoforms norms file.

					self.genes_results([line[0]]) = {isoform_id[]}
			else:
				for line in reader:
					arrayify = line[3].split(",") #arrafiy is a list of transcript ids. they match to isoforms norms file.
					self.genes_results[line[0]] = arrayify;
		'''
#############################
#Reading in the file_manifest
#############################

fileInCabinet = False; #this boolean is to let us know if we found the barcode name in the cabinet.
importantLine = False; #this boolean is to let us know if the line we read is important!
placeHolder = -1; #if the barcode is in the cabinet, then this number will be it's index.
i = 0; #count lines read by script.

with open(manifestFile, 'rb') as f:
	reader = csv.reader(f, delimiter="\t")
	print "Reading in file_manifest, line by line..."
	for line in reader:
		i = i+1 #update count!
		for name in filenameKeywords:
			if name in line[6]:#remove top 3 rows, and also two quantification filename_barcodes per barcode b/c unnecessary
				print "\nLine", i,"from manifest. barcode:", line[5], "\n\t\tfilename: ",line[6].split("rsem.",1)[1]
				importantLine = True;
				for l in cabinet: #search the cabinet
					if (line[5] == l.barcode): #the barcode is already in cabinet.
						placeHolder = cabinet.index(l); #find position of the TissueSample
						fileInCabinet = True;
						print "\t\tFound the TissueSample in cabinet! placeHolder: ", placeHolder
								#this needs to be after the for loop searching cabinet.
								#b/c we search the whole cabinet for the file.
				if (fileInCabinet == True): # the barcode is already there!
					if "genes.normalized" in line[6]:
						cabinet[placeHolder].add_genes_norms(line[6])
					elif "genes.results" in line[6]:
						cabinet[placeHolder].add_genes_results(line[6]);
					elif "isoforms.normalized" in line[6]:
						cabinet[placeHolder].add_isoforms_norms(line[6]);
					fileInCabinet = False #now search is done, reset this indicator for next barcode.
				else: #otherwise, the barcode is not in Cabinet.
					x = TissueSample(line[5]) #We make an new instance of the object, with tissue sample.
					if "genes.normalized" in line[6]:
						x.add_genes_norms(line[6])
					elif "genes.results" in line[6]:
						x.add_genes_results(line[6])
					elif "isoforms.normalized" in line[6]:
						x.add_isoforms_norms(line[6])
					cabinet.append(x) #and add it to the cabinet.
		if (importantLine == True):
			importantLine = False;
		else:
			print "\nLine",i,"does not contain a barcode or proper filename\n"
print "Now printing all genes and normcounts to console. They have already been printed to geneSequenceResults.db in this directory."
print "\tThis will take about 5 minutes... "
cur.execute("SELECT * FROM genes") #this is basic mysqlite and it's pretty simple!
rows = cur.fetchall()
for row in rows:
	print row
print "Above is the database printed out to console."
#Printing the cabinet to console!
print '-' * 55
#for l in cabinet:
	#print "\tcase:",cabinet.index(l),l.barcode, l.genes_results['filename'].split("rsem.",1)[1], l.genes_norms['filename'].split("rsem.",1)[1], l.isoforms_norms['filename'].split("rsem.",1)[1],l.tissue_type,'\n'
print '--length of cabinet: ', len(cabinet), "tissue samples."


con.commit()
con.close()
