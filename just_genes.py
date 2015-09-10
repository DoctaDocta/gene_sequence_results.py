import csv
# we will fill this Cabinet list with objects of TissueSample..
cabinet = []

manifestFile = "TCGA CHOL RNA-seq/file_manifest.txt"; #this is the manifest file path. it has barcode names and filenames.
#append this before each barcode filename so python can find the file.
pathToDataFiles = "TCGA CHOL RNA-seq/RNASeqV2/UNC__IlluminaHiSeq_RNASeqV2/Level_3/"


filenameKeywords = ["genes.results","genes.normalized","isoforms.normalized"]
