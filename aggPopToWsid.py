def aggregatePop(incsv, outdir, template)
    # csv of form UniqueID,Shed,BlockPop
    indir = os.path.split(incsv)[0]
    inname = os.path.splitext(os.path.basename(incsv))[0]
    outcsv = outdir + os.sep + inname + "_byWSID.csv"
    intable = []
    
    # initialize wsid list and create dictionary for later use
    wsidList = template.wsidList
    wsidDict = template.wsidDict

    # open csv and put into array
    fin = open(incsv, 'rb')
    reader = csv.dictreader(fin)
    reader.next()  #skip header row
    
    outtable = template.newCustomTable(wsidList, [Shed,Pop])
    
    for row in reader:
        wsidIndex = wsidDict[row['Shed']]
        outtable[wsidIndex][1] += row['BlockPop']
    
    fin.close()
    return outtable