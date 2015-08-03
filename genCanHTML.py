from genHTMLhelper import genTablesorterJava,genShowHideJava,addrollover,genSubTable,genAbout,genFooter,genHTMLHead,insert_thousands_separator,round_float_to_int,format_total_vals
from unidecode import unidecode
from resources import ordinal

def genHeader(wsid, wsNameDict, wsidDict, totalRankTable):
    header = '	<div id="header">\n\
		<img src="http://web.uvic.ca/~carex/files/logo_vert.png" alt="Logo"\
        width="100" height="100" class="logo" />\n\
        <div id="info">\n\
        <p class="tw-b"><span class="txt16pt"><br>Canada</span><br><br>\n\
        <a href="' + wsid + '_summary.pdf" target="_blank">PDF Summary Report</a>\n\
        </p>\n\
        </div>\n\
        <div id="distribution"></div>\n\
	</div>\n'
    return header

def genMain(wsid, t, totalTable, rankTable, subNameDict, weblinks, tfDict):
    subTable = "	<div id=\"mainContent_wshed\">\n\
    <hr>\n\
    <p>These rankings are based on emissions  to air reported to the National Pollutant Release Inventory in 2006 and our best estimates of emissions from motor vehicles, trains, airplanes taking off and landing, hazardous waste incinerators, and residential heating (oil, gas, and wood). Other sources of these known or suspected carcinogens may exist, and other pollutants not listed here may be emitted from these sources.</p>\n\
    <p><strong>NOTE: </strong>A high rank does not necessarily indicate a high health risk.  Visit the main CAREX environmental estimates for more information on actual measured levels and potential health risk for different substances.</p>\n\
    <table width=\"100%\" cellpadding=\"4\" cellspacing=\"0\" id=\"subTable\" class=\"tablesorter\">\n\
        <thead>\n\
        <tr>\n\
            <th>SUBSTANCE</th>\n\
            <th>ANNUAL AMOUNT (Kg)<br><em>Click for Sources</em></th>\n\
            <th>TOXICITY<br>FACTOR</th>\n\
            <th>TOXIC EQUIVALENT (Kg)<em> Compared to Benzene</em></th>\n\
        </tr>\n\
        </thead>\n\
        <tbody>\n"
    
    for substance in t.subList:
        total = format_total_vals(totalTable[t.wsidDict[wsid]][t.subDict[substance]])
        tftotal = format_total_vals(totalTable[t.wsidDict[wsid]][t.subDict[substance] + 1])
        
        if weblinks.getlink(substance) is not None:
            link = "<a href=\"" + weblinks.getlink(substance) +  "\" target=\"_blank\">" + subNameDict[substance] + "</a>"
        else:
            link = subNameDict[substance]
        
        subTable += "		<tr>\n\
            <td>" + link + "</td>\n\
            <td><a href=\"javascript:ShowContent(\'{" + wsid + "_" + substance + \
            "}\')\">" + total + "</a></td>\n\
            <td>" + tfDict[substance] + "</td>\n\
            <td>" + tftotal + "</td>\n\
        </tr>\n"

    subTable += "		</tbody>\n\
    </table>\n\
    </div>\n"

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

def genWrapper(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, tfDict):
    
    subList = t.subList
    subDict = t.subDict
    wsidDict = t.wsidDict
    totalTable = icube.rTotalTable
    totalRankTable = icube.totalRankTable
    rankTable = icube.rankTable
    infoCube = icube.infoCube
    
    wrapper = "<div id=\"wrapper\">\n"
    
    wrapper += genHeader(wsid, wsNameDict, t.wsidDict, totalRankTable)
#	wrapper += genAbout()
    wrapper += genMain(wsid, t, totalTable, rankTable, subNameDict, weblinks, tfDict)
#	wrapper += genFooter()
    wrapper += genEmitDivs(wsid, t, sourceList, infoCube, sourceDict, subNameDict)
    wrapper += "</div>\n"
    
    return wrapper

def genHTMLBody(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, tfDict):
    htmlbody = "<body>\n"
    htmlbody += genWrapper(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, tfDict)
    htmlbody += genTablesorterJava(t.subList) + genShowHideJava()
    htmlbody += "</body>\n"
    
    return htmlbody

def genCanHTML(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, tfDict):
    html = "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n\
    <html xmlns=\"http://www.w3.org/1999/xhtml\">\n"
    html += genHTMLHead()
    html += genHTMLBody(wsid, t, sourceList, icube, sourceDict, subNameDict, wsNameDict, weblinks, tfDict)
    html += "</html>"
    
    return html
    

