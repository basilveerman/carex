This program consists of the following files:

Primary Invocation:
RUNME.bat
master.py

Pointlayers:
pointMaster.py
genNpriHTML.py
genFcsiHTML.py
genAirHtml.py
genMedIncHtml.py
resources.py

WshedLayers:
wshedMaster.py
aggToWsid.py
genWshedHTML.py
resources.py

INPUT

Specified in the master.py file.  There need to be seperate folders for the point data and the wshed data.

POINTDATA

All point layers being input must be of *.csv format.  Point layers do not have a set data type therefore all accepted point layers must have an entry in the "layers.txt" file with a line item of the form "NAME,CSVFILE".  This file is used to identify the incoming csv and process it accordingly.  If the data format of any point layers is changed, all functions regarding that layer will need to be updated to account for any moved columns.

WATERSHED DATA

All data must be in CSV for following the style of template.txt, with the Title being the name of the source you want displayed in the final html.

subNames.txt - a 2 column csv to translate the template headings to presentable names
webLinks.txt - a 2 column csv to generate/modify which substances have links and what page they link to
wshedNames.txt - a 2 column csv to translate the wshed ID's to proper names