from genHTMLhelper import *
from unidecode import unidecode
from resources import ordinal

def genHeader(wsid, wsNameDict, wsidDict, totalRankTable, popDict):
    imgref = '../healthcharts/' + wsid + '.png'
    header = '	<div id="header">\n\
        <img src="http://web.uvic.ca/~carex/files/logo_vert_150.png" alt="Logo"\
        width="150" height="150" class="logo" />\n\
        <div id="info">\n\
        <h1>Health Region</h1>\n\
        <h4>\n\
        ' + unidecode(wsNameDict[wsid]) + '<br />\n'
    if popDict:
        header += '     Reported Population: ' + insert_thousands_separator(int(popDict[wsid])) + '<br />\n'
    else:
        header += "<br>\n"
    header += '     </h4>\n\
        </div>\n\
        <div id="distribution"><img src="' + imgref + '" width="125%" height="125%"></div>\n\
    </div>\n'
    return header

def genEmitDiv(wsid, t, sourceList, infoCube, sourceDict, subNameDict, substance):
    emitDiv = "\
    <table border=\"0\" cellspacing=\"0\" class=\"sources\">\n\
    <thead>\n\
    <tr>\n\
        <th>Source</th>\n"
    for source in sourceList:
        emitDiv += "		<th>" + source + "</th>\n"
    
    emitDiv += "	</tr>\n\
    </thead>\n\
    <tbody>\n\
    <tr>\n\
        <td>Annual Amount (kg)</td>\n"
    for source in sourceList:
        emitDiv += "        <td>" + format_total_vals(infoCube[sourceDict[source]][t.wsidDict[wsid]][t.subDict[substance]]) + "</td>\n"

    emitDiv += "	</tr>\n		</tbody>\n\
    </table>\n"

    return emitDiv

def genMain(wsid, t, totalTable, rankTable, subNameDict, sourceList, infoCube, sourceDict):
    subTable = '	<div id="mainContent_wshed">\n\
        <p align="center">\n'
    
    progress = 0
    substances = t.subList
    substances.sort()
    
    for substance in substances:
        if progress % 5 != 0: 
            subTable += "  -  "
        else: 
            subTable += "<br>\n"		
        subTable += "<a href=\"#" + substance + "\">" + subNameDict[substance] + "</a>"
        progress += 1
    
    for substance in substances:
        total = format_total_vals(totalTable[t.wsidDict[wsid]][t.subDict[substance]])
        tftotal = format_total_vals(totalTable[t.wsidDict[wsid]][t.subDict[substance] + 1]) 
        rank = ordinal(rankTable[t.wsidDict[wsid]][t.subDict[substance]])
        numranked = str(rankTable[-1][t.subDict[substance]])
        
        subTable += "</p>\n\
    <table id=\"" + substance + "\" width=\"100%\" style=\"page-break-inside: avoid; border-top:2px solid #808080\"><tr><td>\n\
    <table width=\"100%\" cellspacing=\"0\" class=\"summary_sub\">\n\
        <thead>\n\
        <tr>\n\
            <th width=\"25%\">Substance</th>\n\
            <th width=\"25%\">Annual Amount (kg)</th>\n\
            <th width=\"25%\">Toxic Equivalent (Kg)</th>\n\
            <th width=\"25%\">Rank</th>\n\
        </tr>\n\
        </thead>\n\
        <tbody>\n"
        
        subTable += "		<tr>\n\
            <td>" + subNameDict[substance] + "</td>\n\
            <td>" + total + "</td>\n\
            <td>" + tftotal + "</td>\n\
            <td>" + rank + " of " + numranked + "</td>\n\
        </tr>\n\
        </tbody>\n\
    </table>\n\
    </td></tr>\n\
    <tr><td>\n"
        subTable += genEmitDiv(wsid, t, sourceList, infoCube, sourceDict, subNameDict, substance)
        subTable += '</td></tr></table>\n'
    subTable += "</div>\n"

    return subTable

def genWrapper(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, popDict):
    
    totalTable = icube.rTotalTable
    totalRankTable = icube.totalRankTable
    rankTable = icube.rankTable
    infoCube = icube.infoCube
    
    wrapper = "<div id=\"summary_report\">\n"
    
    wrapper += genHeader(wsid, wsNameDict, t.wsidDict, totalRankTable, popDict)
#	wrapper += genAbout()
    wrapper += genMain(wsid, t, totalTable, rankTable, subNameDict, sourceList, infoCube, sourceDict)
#	wrapper += genFooter()
    wrapper += "</div>\n"
    
    return wrapper

def genHTMLBody(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, popDict):
    htmlbody = "<body>\n"
    htmlbody += genWrapper(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, popDict)
    htmlbody += "</body>\n"
    
    return htmlbody

def genHealthSummaryHTML(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, popDict):

    html = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n\
    <html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
    html += genHTMLHead()
    html += genHTMLBody(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, popDict)
    html += "</html>"
    
    return html
    

