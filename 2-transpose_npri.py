#!/usr/bin/python

import os
import glob
import csv
import argparse
import sys

from subprocess import call, check_output, STDOUT
from collections import defaultdict

from resources import ensureDir, convertTF

parser = argparse.ArgumentParser(description='Split aggregation units')
parser.add_argument('indir', help='Input Directory')
parser.add_argument('outdir', help='Output directory')
args = parser.parse_args()

args.indir = os.path.abspath(args.indir)
args.outdir = os.path.abspath(args.outdir)

fields = ['Buta_kg','Buta_TQ','Benz_kg','Benz_TQ','Form_kg','Form_TQ','Perc_kg','Perc_TQ','Chlor_kg','Chlor_TQ','Dichlor_kg','Dichlor_TQ','Acet_kg','Acet_TQ','PCB_kg','PCB_TQ','Ethylb_kg','Ethylb_TQ','Tcdd_kg','Tcdd_TQ','Ars_kg','Ars_TQ','Cadm_kg','Cadm_TQ','Hexcr_kg','Hexcr_TQ','Lead_kg','Lead_TQ','Nick_kg','Nick_TQ','BAA_kg','BAA_TQ','BBF_kg','BBF_TQ','BKF_kg','BKF_TQ','BAP_kg','BAP_TQ','Indeno_kg','Indeno_TQ','Chrys_kg','Chrys_TQ','Pm25_kg','Pm25_TQ']

agg = {
    'abcomm': 'Ab_id',
    'city': 'City_id',
    'ecozone': 'Eco_id',
    'health': 'HR_id',
    'prov': 'Prov_id',
    'wshed': 'WSHED'
}

subdict = {
    'PM2.5 - Particulate Matter <= 2.5 Microns': 'Pm25_kg',
    'Hexavalent chromium (and its compounds)':'Hexcr_kg',
    'Cadmium (and its compounds)':'Cadm_kg',
    'Lead (and its compounds)':'Lead_kg',
    'Formaldehyde':'Form_kg',
    'Acetaldehyde':'Acet_kg',
    'Chloroform':'Chlor_kg',
    'Nickel (and its compounds)':'Nick_kg',
    'Arsenic (and its compounds)':'Ars_kg',
#    'Chromium (and its compounds)':'Chrom_kg',
    'Indeno(1,2,3-c,d)pyrene - PAH':'Indeno_kg',
    'Benzo(k)fluoranthene - PAH':'BKF_kg',
    'Benzo(b)fluoranthene - PAH':'BBF_kg',
    'Benzo(a)anthracene - PAH':'BAA_kg',
    'Benzo(a)pyrene - PAH':'BAP_kg',
    'Benzo(a)phenanthrene - PAH':'Chrys_kg',
    'Benzene':'Benz_kg',
    'Ethylbenzene':'Ethylb_kg',
    'Dichloromethane':'Dichlor_kg',
    '1,3-Butadiene':'Buta_kg',
    'Tetrachloroethylene':'Perc_kg'
}

header = {}
for x in agg.keys():
    header[x] = ['UniqueID', agg[x]] + fields

print "Transposing NPRI sources in  {}".format(args.indir)

for key in agg.keys():
    infile = os.path.join(args.indir, key, 'NPRI_' + key + '_intermediate.csv')
    print os.path.basename(infile)
    with open(infile, 'rb') as f:
        reader = csv.DictReader(f)
        progress = 1
        done = float(check_output(['wc', '-l', infile]).split()[0])

        # go through aggregation keys appending to appropriate data structre
        output = []
        for line in reader:
            progress += 1
            sys.stdout.write("\r{:.2%}".format(progress/done))
            sub = line['CHEM_E']
            if sub not in subdict: continue
            emissions = float(line['Total_kg'])
            teq = convertTF(emissions, subdict[sub])
            output.append({agg[key]: line[agg[key]], subdict[sub]: emissions, subdict[sub].split('_')[0] + '_TQ': teq})

    print '\n' + key + ': ' + str(len(output))
    ensureDir(os.path.join(args.outdir, key))
    outfile = os.path.join(args.outdir, key, 'Industrial Emitters.csv')

    with open(outfile, 'wb') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=header[key])
        writer.writeheader()
        writer.writerows(output)

    print ' -- DONE PROCESSING FILE'


    


