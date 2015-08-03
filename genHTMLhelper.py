city_disclaimer = '\n\
    <hr>\n\
    <p>These rankings are based on emissions  to air reported to the National Pollutant Release Inventory in 2011 and our best estimates of emissions from motor vehicles, trains, airplanes taking off and landing, and residential heating (oil, gas, and wood) within 25km. Other sources of these known or suspected carcinogens may exist, and other pollutants not listed here may be emitted from these sources.</p>\n\
    <p><strong>NOTE: </strong>A high rank does not necessarily indicate a high health risk.  Visit the main CAREX environmental estimates for more information on actual measured levels and potential health risk for different substances.</p>\n'


disclaimer = '\n\
    <hr>\n\
    <p>These rankings are based on emissions  to air reported to the National Pollutant Release Inventory in 2011 and our best estimates of emissions from motor vehicles, trains, airplanes taking off and landing, and residential heating (oil, gas, and wood). Other sources of these known or suspected carcinogens may exist, and other pollutants not listed here may be emitted from these sources.</p>\n\
    <p><strong>NOTE: </strong>A high rank does not necessarily indicate a high health risk.  Visit the main CAREX environmental estimates for more information on actual measured levels and potential health risk for different substances.</p>\n'

def genTablesorterJava(subList):
    tablesorter = "<script type=\"text/javascript\">\n\
    $(\"document\").ready(function() {\n\
        $(\"#subTable\").tablesorter( {\
widgets: ['zebra'],\
sortList: [[0,0]]\
});\n"
    for substance in subList:
        tablesorter += "\
        $(\"#" + substance + "Table\").tablesorter( {\
widgets: ['zebra'],\
sortList: [[0,0]]\
});\n"
    
    tablesorter += "    });\n</script>\n"
    return tablesorter

def genShowHideJava():
	showhide = "<script type=\"text/javascript\" language=\"JavaScript\"><!--\n\
	function HideContent(d) {\n\
	if(d.length < 1) { return; }\n\
	document.getElementById(d).style.display = \"none\";\n\
	}\n\
	function ShowContent(d) {\n\
	if(d.length < 1) { return; }\n\
	document.getElementById(d).style.display = \"block\";\n\
	}\n\
	//--></script>\n"
	return showhide

def addrollover(case):
    if case == 'Not Expected':
        r = 'This source is not generally expected to contribute emissions of this substance'
    elif case == 'No Emission Factor':
        r = 'There are no published Emission Factors for this substance from this source'
    s = '<a class="rollover" href="#"><u>' + case + '</u><span>' + r + '</span></a>'
    return s

def genSubTable(wsid, t, totalTable, rankTable, subNameDict, weblinks, tfDict, title):
    subTable = '''<table width="100%" cellpadding="4" cellspacing="0" id="subTable" class="tablesorter">\n\
        <thead>\n\
        <tr>\n\
            <th>SUBSTANCE</th>\n\
            <th>ANNUAL AMOUNT (Kg)<br><em>Click for Sources</em></th>\n\
            <th>TOXICITY<br>FACTOR</th>\n\
            <th>TOXIC EQUIVALENT (Kg)<em> Compared to Benzene</em></th>\n\
            <th>SUBSTANCE RANK</th>\n\
            <th>{title}</th>\n\
        </tr>\n\
        </thead>\n\
        <tbody>\n'''.format(title=title)
    
    for substance in t.subList:
        total = format_total_vals(totalTable[t.wsidDict[wsid]][t.subDict[substance]])
        tftotal = format_total_vals(totalTable[t.wsidDict[wsid]][t.subDict[substance] + 1])
        rank = str(rankTable[t.wsidDict[wsid]][t.subDict[substance]])
        numranked = str(rankTable[-1][t.subDict[substance]])
        
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
            <td>" + rank + "</td>\n\
            <td>" + numranked + "</td>\n\
        </tr>\n"
    subTable += "		</tbody>\n\
    </table>\n"
    return subTable

def genAbout():
	about = "	<div id=\"about\">\n\
		<p>CAREX Canada is a multidisciplinary team of researchers based at the School of Environmental Health, University of British Columbia. The team has expertise in epidemiology, occupational hygiene, geographic information systems, and knowledge transfer and exchange.</p>\n\
		<p><a href=\"http://www.carexcanada.ca\">CAREX Home</a></p>\n\
	</div>\n"
	return about
	
def genFooter():
	footer = "	<div id=\"footer\"></div>\n"
	return footer

	
def genHTMLHead(css='default'):
	cssLink = '<link href="http://web.uvic.ca/~carex/files/ranking_reports.css" rel="stylesheet" type="text/css" />\n'
	htmlhead = "<head>\n\
	<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\n\
	<title>Ranking Report</title>\n"
	
	htmlhead += cssLink
	
	htmlhead +="\n\
	<script type=\"text/javascript\" src=\"http://web.uvic.ca/~carex/files/jquery.min.js\"></script>\n\
	<script type=\"text/javascript\" src=\"http://web.uvic.ca/~carex/files/jquery.tablesorter.js\"></script>\n"

	htmlhead += "</head>"
	return htmlhead

def insert_thousands_separator(d):
    # this function will take an integer or float and return a string
    # with a locale defined thousands seperator
    
    import locale
    locale.setlocale(locale.LC_ALL, '')
    
    if type(d) not in (float, int):
        raise TypeError('Can only insert thousands seperator into floats or ints')
        
    if type(d) == int:
        return locale.format("%d", d, grouping=True)
        
    elif type(d) == float: ## todo: check original precision and round to that amount before return
        return locale.format("%f", d, grouping=True)
    
def round_float_to_int(f):
    if type(f) not in (float, int):
        raise TypeError('Input must be of type float or int')
    return int(round(f,0))
    
def format_total_vals(total):
    if type(total) == str:
        return total
    else:
        ## handle case where value is 0
        if total == 0:
            return '0'
            
        ## handle case where value round to 0
        total = round_float_to_int(total)
        if total == 0: 
            return '&lt; 0.5'
        else:
            return insert_thousands_separator(total)
