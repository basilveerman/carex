# based on an imput csv, this will aggregate the values to watershed ID

import os, csv

def ensureDir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)
    return dir

def testType(input):
    if input == '':
        return 'empty'
    try:
        float(input)
        return 'float'
    except ValueError:
        return 'string'
        
def aggregate(incsv, outdir, template):
    indir = os.path.split(incsv)[0]
    inname = os.path.splitext(os.path.basename(incsv))[0]
    outcsv = outdir + os.sep + inname + "_byWSID.csv"
    intable = []
    
    # initialize wsid list and create dictionary for later use
    wsidList = template.wsidList
    wsidDict = template.wsidDict
    
    # open csv and put into array
    fin = open(incsv, 'rb')
    reader = csv.reader(fin)
    for row in reader: 
        intable.append(row)
    fin.close()
    
    # create destination array
    outtable = template.newTemplateTable()

    # define special values
    sVals = ['No Emission Factor','Not Expected','NA','No TQ','NoTQ']
    
    # detect which fields are special values, which are numeric
    nonNumeric = {}
    numeric = range(2,len(intable[1]))
    fieldIndex = numeric[:]
    for i in fieldIndex:
        testVal = intable[1][i]
        # print i, intable[0][i], testVal
        if testVal in sVals: 
            nonNumeric[i] = testVal
            numeric.remove(i)

    # insert non-numeric values into outtable
    for row in outtable[1:]:
        for col in nonNumeric.keys():
            try:
                row[col-1] = nonNumeric[col]
            except Exception, e:
                print row
                print col
                raise e
    
    # insert numeric values into outtable, keeping track of which wsid's had info
    # this section will have to take care of 9 possible cases
    # 	outable 	intable	result
    #	0		''		'Not Estimated'
    #	0		string	string
    #	0		number	number
    #	string	''		no chnage
    #	string	string	no change
    #	string	number	number
    #	number	''		no change
    #	number	string	no change
    #	number	number	number + number
    noSources = wsidList[:]
    inSize = len(intable)
    progress = 0
    for row in intable[1:]:
        if inSize > 10000 and progress % 10000 == 0:
            print "           " + str(progress) + " of " + str(inSize)
        try:
            noSources.remove(row[1])
        except: pass  # if wsid has already been removed supress error
        
        try:
            wsidIndex = wsidDict[row[1]]
        except KeyError as e:
            if row[1] == '88':
                continue
            else:
                raise e

        for colIndex in numeric:
            
            if outtable[wsidIndex][colIndex -1] == 0:
                if testType(row[colIndex]) == 'empty':
                    outtable[wsidIndex][colIndex -1] = 'Not Estimated'
                elif testType(row[colIndex]) == 'string':
                    outtable[wsidIndex][colIndex -1] = row[colIndex]
                elif testType(row[colIndex]) == 'float':
                    outtable[wsidIndex][colIndex -1] = float(row[colIndex])
            
            elif type(outtable[wsidIndex][colIndex -1]) == str:
                if testType(row[colIndex]) == 'empty':
                    pass
                elif testType(row[colIndex]) == 'string':
                    pass
                elif testType(row[colIndex]) == 'float':
                    outtable[wsidIndex][colIndex -1] = float(row[colIndex])
                
            elif type(outtable[wsidIndex][colIndex -1]) == float:
                if testType(row[colIndex]) == 'empty':
                    pass
                elif testType(row[colIndex]) == 'string':
                    pass
                elif testType(row[colIndex]) == 'float':
                    outtable[wsidIndex][colIndex -1] += float(row[colIndex])
        progress +=1

    # detect watersheds that did not have any sources and insert "not present"
    for wsid in noSources:
        for colIndex in range(2,len(intable[1])):
            if outtable[wsidDict[wsid]][colIndex-1] == 'No TQ':
                continue
            elif outtable[wsidDict[wsid]][colIndex-1] == 'NoTQ':
                continue
            else:
                outtable[wsidDict[wsid]][colIndex-1] = "Source Not Present"
    
    fout = open(outcsv, 'wb')
    writer = csv.writer(fout)
    writer.writerows(outtable)
    fout.close()
    
    return outtable

if __name__ == '__main__':
    indir = r'C:\basil\ge_Google_Earth\rawdata\testinput'
    outdir = ensureDir(indir + os.sep + "output")
    incsv = r'C:\basil\ge_Google_Earth\rawdata\testinput\NPRI.csv'

    aggregatePop(incsv, outdir)
