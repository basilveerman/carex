import os, fnmatch, csv
from operator import itemgetter


def ensureDir(dir):
	if not os.path.isdir(dir):
		os.makedirs(dir)
	return dir

def buildCsvList(indir):
	inCsvList = []
	for file in os.listdir(indir):
		if fnmatch.fnmatch(file, '*.csv'):
			inCsvList.append(indir + os.sep + file)
	return inCsvList
	
def genTableFrCsv(incsv):
	table = []
	fin = open(incsv, 'rb')
	reader = csv.reader(fin)
	for row in reader: 
		table.append(row)
	fin.close()
	return table
	
def exportCsv(table, outcsv):
	fout = open(outcsv, 'wb')
	writer = csv.writer(fout)
	writer.writerows(table)
	fout.close()
	
def buildDictFrCsv(incsv, i=0, j=1):
	## based on an input csv, this creates a dictionary based on key in column i and result in column j
	table = []
	fin = open(incsv, 'rb')
	reader = csv.reader(fin)
	for row in reader: 
		table.append(row)
	fin.close()
	
	d = dict([(row[i], row[j]) for row in table])
	return d

def uniqify(seq):
	# this will return a uniqified, order preserved list based on input list
	seen = {}
	result = []
	for item in seq:
		if item in seen: continue
		seen[item] = 1
		result.append(item)
	return result

def sortTable(table, col):
    return sorted(table, key=itemgetter(col))