import os, fnmatch, csv, copy
from aggToWsid import aggregate
from operator import itemgetter
from pygooglechart import XYLineChart, Axis
from collections import defaultdict

tfdict = dict([x.split(',') for x in '''Buta_kg,0.54
Acet_kg,0.017
Ars_kg,2600
BAA_kg,54
BAP_kg,6400
BBF_kg,130
Benz_kg,1
Cadm_kg,28
Chlor_kg,1.6
Chrom_kg,130
Chrys_kg,5.1
Dichlor_kg,0.2
Form_kg,0.02
Indeno_kg,280
Lead_kg,28
Nick_kg,2.8
Perc_kg,0.92
Tcdd_kg,1.2e9'''.split('\n')])

for sub in tfdict:
    tfdict[sub] = float(tfdict[sub])

# BKF_kg,NO TF
# Ethylb_kg,NO TF
# PCB_kg,NO TF
# Pm25_kg,NO TF
# Hexcr_kg,NO TF

def convertTF(val, sub):
    if sub in tfdict:
        return val*tfdict[sub]
    else:
        return 'No TF'

class population:
    def __init__(self, incsv, template):
        self._popInput = []
        
        fin = open(incsv, 'rb')
        reader = csv.DictReader(fin)
        for row in reader:
            self._popInput.append(row)
        fin.close()
        
        self.popTable = template.newCustomTable(template.wsidList, ['Shed','Pop'])
        self.wsidList = template.wsidList
        self.wsidDict = template.wsidDict

        for row in self._popInput[1:]:
            self.wsidIndex = self.wsidDict[row['Shed']]
            self.popTable[self.wsidIndex][1] += int(row['BlockPop'])
        
        self.popDict = buildDictFrTable(self.popTable)
        
class newTemplate:
    def __init__(self, incsv):
        self.infile = incsv
        fin = open(incsv, 'rb')
        reader = csv.reader(fin)
        self.intable = []
        for row in reader: 
            self.intable.append(row)
        fin.close()
    
        # create field list and dictionary, omitting 1st col of uniqueID
        self.fieldList = self.intable[0][1:]
        self.fieldDict = dict([(field, self.fieldList.index(field)) for field in self.fieldList])
        # create wsidList
        self.wsidList = []
        for i in range(1,len(self.intable)):
            self.wsidList.append(self.intable[i][1])
        self.wsidDict = dict([(wsid, self.wsidList.index(wsid) + 1) for wsid in self.wsidList])
        
        # extract sub list from fields and set dictionary
        self.subList = [self.fieldList[i] for i in range(1,len(self.fieldList),2)]
        self.subDict = self.fieldDict
    
    def newTemplateTable(self):
        table = [[]]
        header = self.fieldList[:]
        data = [ [0 for i in range(len(header))] for j in range(len(self.wsidList))]
        i = 0
        for wsid in self.wsidList:
            data[i][0] = wsid
            i += 1
            
        table[0] = header
        table += data
        
        return table
        
    def newCustomTable(self, rowList, colList):
        table = [[]]
        header = colList[:]
        data = [ [0 for i in range(len(header))] for j in range(len(rowList))]
        for wsid in rowList:
            data[rowList.index(wsid)][0] = wsid
            
        table[0] = header
        table += data
        
        return table	

class newInfoCube:
    ## instantiating this object only create the placehoder for the info cube
    ## upon calling the build fucntion, this creates self.infocube then creates 4 key elements:
    ## self.totalTable
    ## self.rTotalTable - total table rounded to 1 decimal place
    ## self.rankTable - ranks by wsid for each substance
    ## self.totalRankTable - overall watershed ranks
    def __init__(self,):
        self.infoCube = []
    def build(self, inCsvList, outdir, sourceList, template):
        self.inCsvList = inCsvList
        self.buildIcube(inCsvList, outdir, template)
        self.buildTotalTable(sourceList, template)
        self.roundTotalTable(self.totalTable)
        self.buildRanksBySub(outdir, template)
        self.buildTotalRanks(template)
    
    def buildIcube(self, inCsvList, outdir, template):
        for inCsv in inCsvList:
            print "Processing " + os.path.basename(inCsv)
            self.infoCube.append(aggregate(inCsv, outdir, template))
            print "           DONE"
    
    def buildTotalTable(self, sourceList, template):
        print "Generating Totals..."
        self.totalTable = template.newTemplateTable()
        ## Generate a totals table, handling special values accordingly
        for table in self.infoCube:
            print "\t" + self.inCsvList[self.infoCube.index(table)]
            for rowI in range(1, len(table)):
                for colI in range(1, len(table[rowI])):
                    if table[rowI][colI] == 'No TQ' or table[rowI][colI] == 'NoTQ' or table[rowI][colI] == 'No TEQ':
                        self.totalTable[rowI][colI] = 'No TQ'
                    try:
                        self.totalTable[rowI][colI] += float(table[rowI][colI])
                    
                    ## when table contains text, skip that entry
                    except ValueError: pass
                    
                    ## raise and stop when trying to overwrite extisting text in total table
                    except TypeError as e:
                        print "Already in total table: " + self.totalTable[rowI][colI]
                        print "Trying to add: {} From row: {} col: {}".format(str(table[rowI][colI]), str(rowI), str(colI))
                        print table[rowI]
                        print "Source: " + self.inCsvList[self.infoCube.index(table)]
                        raise e
                        
        ## now handle 0 values in total table
        for rowI in range(1, len(self.totalTable)):
            for colI in range(1, len(self.totalTable[rowI])):
                if self.totalTable[rowI][colI] == 0:
                    self.totalTable[rowI][colI] = "See Info"
        print "DONE" 
        
    def roundTotalTable(self, table):
        print "Rounding Totals...",
        self.rTotalTable = copy.deepcopy(table)
        ## round values in input table to 1 decimal
        for rowI in range(len(self.rTotalTable)):
            for colI in range(len(self.rTotalTable[rowI])):
                if type(self.rTotalTable[rowI][colI]) == float:
                
                    ## account for cases in which a source exists but there are no emissions
                    if self.rTotalTable[rowI][colI] == 0:
                        self.rTotalTable[rowI][colI] = "Source Not Present"
                    
                    ## if above 0, round to integer
                    self.rTotalTable[rowI][colI] = int(round(self.rTotalTable[rowI][colI],0))
                    if self.rTotalTable[rowI][colI] == 0:
                        self.rTotalTable[rowI][colI] = "< 0.5"
        print "DONE"

    def buildRanksBySub(self, outdir, template):
        print "Generating Substance Ranks...",
        self.rankTable = template.newTemplateTable()
        self.subChartData = defaultdict(list)
        
        fieldList = template.fieldList
        subList = template.subList
        subDict = template.subDict
        wsidDict = template.wsidDict
        
        ## add another row to track total number ranked for each substance
        numRanked = [0 for i in range(len(fieldList))]
        numRanked[0] = "TotalNoRanked"
        self.rankTable.append(numRanked)
        
        for substance in subList:
            
            tempTable = sortTable(self.totalTable, subDict[substance])
            exportCsv(tempTable, outdir + os.sep + "rankT_" + substance + ".csv")
            rankList = []
            ## extract a the low to high list of wsid's, skipping non-floats (no measurement)
            for row in tempTable:
                if type(row[subDict[substance]]) == float:
                    rankList.append(row[0]) ## build wsid list in ranked order
                    self.subChartData[substance].append(row[subDict[substance]])
            numRanked[subDict[substance]] = len(rankList)
            
            ## by default, this ranks low to high, we want to rank high to low starting at 1
            rankList.reverse()
            
            ## with the list of ranked wsids, get the rank and save to rankTable
            for rank, wsid in enumerate(rankList): 
                self.rankTable[wsidDict[wsid]][subDict[substance]] = rank + 1

        ## any 0 (default) values become 'NR' - No Rank
        for rowI in range(len(self.rankTable)):
            for colI in range(len(self.rankTable[rowI])):
                if self.rankTable[rowI][colI] == 0:
                    self.rankTable[rowI][colI] = "NR"
        print "DONE"

    # def genSubCharts(self, outdir, template):
        # self.subChartDict = {}
        # for sub in template.subList:
            # for wsid in template.wsidList:
                # print '#' * 40
                # print wsid, sub
                # outfile = outdir + os.sep + wsid + sub + '.png'
                # if type(self.totalTable[template.wsidDict[wsid]][template.subDict[sub]]) == float: 
                    # val = self.totalTable[template.wsidDict[wsid]][template.subDict[sub]]
                # else:
                    # val = 0
                # width = 100
                # height = 25
                # self.subChartDict[(sub, wsid)] = genChart(width, height, self.subChartData[sub], val, outfile)
            
    def buildTotalRanks(self, template):
        print 'Generating Total Ranks...',
        self.totalRankTable = template.newCustomTable(template.wsidList, ['Shed','Total TQ','Rank'])
        self.wshedChartData = []
        self.wshedChartIndex = {}

        for wsid in template.wsidList:
            for substance in template.subList:
                tqval = self.totalTable[template.wsidDict[wsid]][template.subDict[substance] + 1]
                if type(tqval) == float:
                    self.totalRankTable[template.wsidDict[wsid]][1] += tqval
        
        for row in self.totalRankTable:
            if row[1] == 0:
                self.totalRankTable[self.totalRankTable.index(row)][1] = "No TQ"
                
        sortedtable = sortTable(self.totalRankTable, 1)
        
        rankList = []
        for row in sortedtable:
            if type(row[1]) == float:
                rankList.append(row[0])
                self.wshedChartData.append(int(row[1]) + 1000000)  # add set value to bring off x axis
                self.wshedChartIndex[row[0]] = sortedtable.index(row)
        self.numRanked = len(rankList)
        
        ## by default, this ranks low to high, we want to rank high to low starting at 1
        rankList.reverse()
        
        for rank, wsid in enumerate(rankList): 
            self.totalRankTable[template.wsidDict[wsid]][2] = rank + 1	
            
        for rowI in range(len(self.totalRankTable)):
            if self.totalRankTable[rowI][2] == 0:
                self.totalRankTable[rowI][2] = 'NR'
                
        self.totalRankTable.append(["bogus","bogus",self.numRanked])
        print "DONE"
    
    def genWshedCharts(self, outdir, template, title):
        print "Generating Ranking Charts..."
        self.wshedChartDict = {}
        progress = 0
        for wsid, index in template.wsidDict.iteritems():
            if progress % 5 == 0: print '\t\t' + str(progress) + ' of ' + str(len(template.wsidList))
            outfile = outdir + os.sep + wsid + '.png'
            try:
                ind = self.wshedChartIndex[wsid]
            except KeyError:
                ind = 0
            width = 260
            height = 100
            self.wshedChartDict[wsid] = genChart(width, height, self.wshedChartData, ind, outfile, title)
            progress += 1
        print "           DONE"
		
def validFileName(s):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    
    Adapted From Django's "django/template/defaultfilters.py".
    """
    import re
    from unidecode import unidecode
    
    _slugify_strip_re = re.compile("[^\w\s'-]")
    _slugify_hyphenate_re = re.compile(r'[-\s]+')
    
    if not isinstance(s, unicode):
        s = unicode(s)
    s = unidecode(s)
    return unicode(_slugify_strip_re.sub('', s).strip())
        
def genChart(width, height, data, ind, outfile, title):
    # this is designed to take a list, the value of the wshed, and save the output graph
    mn = min(data)
    mx = max(data)
    chart = XYLineChart(width, height, title=title, x_range=(0,len(data)), y_range=(0,mx))
    chart.set_colours(['3072F3','FF0000'])
    chart.set_line_style(0,3)
    chart.set_grid(20,25,1,5)
    # set up axis and labels
    left_axis = chart.set_axis_labels(Axis.LEFT, ['            Lowest','Total Toxicity    ','            Highest'])
    chart.set_axis_style(left_axis, '202020', font_size=11, alignment=0)
    #add x and y data for distribution line
    chart.add_data(range(len(data)))
    chart.add_data(data)

    #add marker to position of ind
    chart.add_marker(0, ind, 'd', 'FF0000', 10)
    
    chart.download(outfile)
    return outfile

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

def buildSourceList(inCsvList):
    sourceList = []
    for csv in inCsvList:
        sourceList.append(os.path.splitext(os.path.basename(csv))[0])
    return sourceList
    
def sortTable(table, col):
    return sorted(table, key=itemgetter(col))
    
def buildDictFrCsv(incsv, i=0, j=1):
    ## based on an input csv, this creates a dictionary based on key in column i and result in column j
    table = genTableFrCsv(incsv)
    return dict([(row[i], row[j]) for row in table])
    
def buildDictFrTable(table, i=0, j=1):
    return dict([(row[i], row[j]) for row in table])

def exportCsv(table, outcsv):
    fout = open(outcsv, 'wb')
    writer = csv.writer(fout)
    writer.writerows(table)
    fout.close()

def genTableFrCsv(incsv):
    table = []
    fin = open(incsv, 'rb')
    reader = csv.reader(fin)
    for row in reader:
        table.append(row)
    fin.close()
    return table
    
def uniqify(seq):
    # this will return a uniqified, stable list based on an input list
    seen = {}
    result = []
    for item in seq:
        if item in seen: continue
        seen[item] = 1
        result.append(item)
    return result

def ordinal(value):
    """
    Converts zero or a *postive* integer (or their string 
    representations) to an ordinal value.

    >>> for i in range(1,13):
    ...     ordinal(i)
    ...     
    u'1st'
    u'2nd'
    u'3rd'
    u'4th'
    u'5th'
    u'6th'
    u'7th'
    u'8th'
    u'9th'
    u'10th'
    u'11th'
    u'12th'

    >>> for i in (100, '111', '112',1011):
    ...     ordinal(i)
    ...     
    u'100th'
    u'111th'
    u'112th'
    u'1011th'

    """
    try:
        value = int(value)
    except ValueError:
        return value

    if value % 100//10 != 1:
        if value % 10 == 1:
            ordval = u"%d%s" % (value, "st")
        elif value % 10 == 2:
            ordval = u"%d%s" % (value, "nd")
        elif value % 10 == 3:
            ordval = u"%d%s" % (value, "rd")
        else:
            ordval = u"%d%s" % (value, "th")
    else:
        ordval = u"%d%s" % (value, "th")

    return ordval
