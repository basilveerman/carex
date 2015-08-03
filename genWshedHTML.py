from genHTMLhelper import genTablesorterJava,genShowHideJava,addrollover,genSubTable,genAbout,genFooter,genHTMLHead,insert_thousands_separator,round_float_to_int,format_total_vals,disclaimer
from unidecode import unidecode
from resources import ordinal

def genHeader(wsid, wsNameDict, wsidDict, totalRankTable, popDict):
    imgref = '../wscharts/' + wsid + '.png'
    header = '''<div id="header">\n\
	<img src="http://web.uvic.ca/~carex/files/logo_vert.png" alt="Logo"\
        width="100" height="100" class="logo" />\n\
        <div id="info">\n\
        <p class="tw-b"><span class="txt16pt" style="margin-bottom:6px">Watershed</span><br>\n\
        ID: {wsid}<br />\n\
        {name}                             <br />\n\
        Reported Population: {pop}<br />\n\
        <a href="{wsid}_summary.pdf" target="_blank">PDF Summary Report</a>\n\
        </p>\n\
        </div>\n\
        <div id="distribution"><img src="{chart}" width="260" height="100" /></div>\n\
	</div>\n'''.format(name = unidecode(wsNameDict[wsid]),
                           pop = insert_thousands_separator(int(popDict[wsid])),
                           wsid = wsid,
                           chart = imgref)
    return header

def genMain(wsid, t, totalTable, rankTable, subNameDict, weblinks, tfDict):
    subTable = "    <div id=\"mainContent_wshed\">" + disclaimer
    subTable += genSubTable(wsid, t, totalTable, rankTable, subNameDict, weblinks, tfDict, "# WATERSHEDS WITH SUBSTANCE")
    subTable += "</div>\n"
    return subTable

def genEmitDivs(wsid, t, sourceList, infoCube, sourceDict, subNameDict):
    emitDivs = ""
    for substance in t.subList:
        emitDivs += "\
        <div id=\"{" + wsid + "_" + substance + "}\" class=\"emitinfo\">\n\
        <p class=\"substance\">Substance: " + subNameDict[substance] + \
        "</p><p><a href=\"javascript:HideContent('{" + wsid + "_" + \
        substance + "}')\" class=\"closebutton\"><span>Close</span></a></p>\n\
        <table width=\"100%\" border=\"0\" cellpadding=\"4\" cellspacing=\"0\" id=\"" + \
        substance + "Table\" class=\"tablesorter\">\n\
        <thead>\n\
        <tr>\n\
            <th>Source</th>\n\
            <th>Annual Amount (kg)</th>\n\
        </tr>\n\
        </thead>\n\
        <tbody>\n"
        for source in sourceList:
            emitted = format_total_vals(infoCube[sourceDict[source]][t.wsidDict[wsid]][t.subDict[substance]])
            if emitted == 'Not Expected':
                emitted = addrollover(emitted)
            elif emitted == 'No Emission Factor':
                emitted = addrollover(emitted)
            emitDivs += "\
            <tr>\n\
            <td>" + source + "</td>\n\
            <td>" + emitted + "</td>\n\
        </tr>\n"
    
        emitDivs += "		<tbody>\n\
        </table>\n\
        </div>\n"

    return emitDivs

def genWrapper(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, popDict, tfDict):
    
    subList = t.subList
    subDict = t.subDict
    wsidDict = t.wsidDict
    totalTable = icube.rTotalTable
    totalRankTable = icube.totalRankTable
    rankTable = icube.rankTable
    infoCube = icube.infoCube
    
    wrapper = "<div id=\"wrapper\">\n"
    
    wrapper += genHeader(wsid, wsNameDict, t.wsidDict, totalRankTable, popDict)
#	wrapper += genAbout()
    wrapper += genMain(wsid, t, totalTable, rankTable, subNameDict, weblinks, tfDict)
#	wrapper += genFooter()
    wrapper += genEmitDivs(wsid, t, sourceList, infoCube, sourceDict, subNameDict)
    wrapper += "</div>\n"
    
    return wrapper

def genHTMLBody(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, popDict, tfDict):
    htmlbody = "<body>\n"
    htmlbody += genWrapper(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, popDict, tfDict)
    htmlbody += genTablesorterJava(t.subList) + genShowHideJava()
    htmlbody += "</body>\n"
    
    return htmlbody

def genWshedHTML(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, popDict, tfDict):

    html = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n\
    <html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
    html += genHTMLHead()
    html += genHTMLBody(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, popDict, tfDict)
    html += "</html>"
    
    return html
    

