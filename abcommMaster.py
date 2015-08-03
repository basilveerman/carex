import os, sys
from genABcommHTML import genABcommHTML
from genABcommSummaryHTML import genABcommSummaryHTML
from genPDF2 import htmlToPdf
from multiprocessing import Process
import cPickle as pickle
from constants import Weblinks
from unidecode import unidecode



from resources import *

def processWshed(args):
    indir = args.indir
    update_data = args.update
    if args.pdf:
        args.summary = True

    outdir = ensureDir(indir + os.sep + "tempfiles")

    ## generate list of full paths to csv's in input directory
    inCsvList = buildCsvList(indir)
        
    ## based on the input csv's, generate a list of sources they represent as well as dictionary for later use
    sourceList = buildSourceList(inCsvList)
    sourceDict = dict([(src, sourceList.index(src)) for src in sourceList])
    
    ## create template based on input file
    template = newTemplate(indir + os.sep + "template.txt")
    
    ## we also need a substance dictionary to later conver the shortnames to presentable names
    subNameDict = buildDictFrCsv(indir + os.sep + "subNames.txt")
    wsNameDict = buildDictFrCsv(indir + os.sep + "community_names.txt")
    weblinks = Weblinks()
    tfDict = buildDictFrCsv(indir + os.sep + "tf.txt")
    popDict = buildDictFrCsv(indir + os.sep + "population.txt")
    
    ## instantiate and build the info cube if new data, else load old data    
    if update_data:
        icube = newInfoCube()
        icube.build(inCsvList, outdir, sourceList, template)
        print "Pickling Data... ",
        pickle.dump(icube, open(outdir + os.sep +"icube.p", "wb"))
        print "DONE"
    else:
        print "Loading previous Data... ",
        icube = pickle.load( open(outdir + os.sep +"icube.p"))
        print "DONE"
    
    chartDir = ensureDir(os.path.dirname(indir) + os.sep + "output" + os.sep + "abcommcharts")
    if args.charts:
        icube.genWshedCharts(chartDir, template, "This Community's Ranking")

    ## export key elements to csv for data checking
    exportCsv(icube.totalTable, outdir + os.sep + "TotalTable.csv")
    exportCsv(icube.rTotalTable, outdir + os.sep + "RoundedTotalTable.csv")
    exportCsv(icube.rankTable, outdir + os.sep + "RankTable.csv")
    exportCsv(icube.totalRankTable, outdir + os.sep + "TotalRanksTable.csv")

    
    wsHtmlDir = ensureDir(os.path.dirname(indir) + os.sep + "output" + os.sep + "abcommhtml")
    inSize = len(template.wsidList)
    
    print "Generating HTML..."
    progress = 0
    for wsid in template.wsidList:
        if progress % 100 == 0:
            print "           " + str(progress) + " of " + str(inSize)
        f = open(wsHtmlDir + os.sep + wsid + ".html", 'w')
        f.write(genABcommHTML(wsid, template, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, popDict, tfDict))
        f.close()
        progress += 1
    print "           DONE"

    if args.summary:
        print "Generating Summary HTML and PDF..."
        progress = 0
        for wsid in template.wsidList:
            if progress % 100 == 0:
                print "           " + str(progress) + " of " + str(inSize)
            name = validFileName(unidecode(wsNameDict[wsid].decode('latin')))
            print name
            # html_summary_path = os.path.join(wsHtmlDir, name + ".html")
            html_summary_path = wsHtmlDir + os.sep + wsid + "_summary.html"
            f = open(html_summary_path, 'w')       
            html = genABcommSummaryHTML(wsid, template, sourceList, icube, sourceDict, subNameDict, wsNameDict, popDict)
            f.write(html.encode('utf-8'))
            f.close()   
            
            if args.pdf:
                # htmlToPdf(html_summary_path,os.path.join(wsHtmlDir, name + ".pdf"))
                htmlToPdf(html_summary_path,wsHtmlDir + os.sep + wsid + "_summary.pdf")
            
            progress += 1
        print "           DONE"	
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process Watershed aggregated data')
    parser.add_argument('-i', '--indir', help='Input directory', required=False,
                        default='/home/bveerman/Personal/CAREX/emp2012/GE/htmlGen/abcomm')
    parser.add_argument('-u', '--update', action='store_true', default=False, help='Output directory')
    parser.add_argument('-c', '--charts', action='store_true', default=False, help='Generate charts')
    parser.add_argument('-s', '--summary', action='store_true', default=False, help='Generate summary html')
    parser.add_argument('-p', '--pdf', action='store_true', default=False, help='Generate summary pdf (must also use -s)')
    args = parser.parse_args()
    processWshed(args)
