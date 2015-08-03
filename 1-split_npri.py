#!/usr/bin/python

import os
import glob
import csv
import argparse
import sys

from subprocess import call, check_output, STDOUT
from collections import defaultdict

from resources import ensureDir

parser = argparse.ArgumentParser(description='Split aggregation units')
parser.add_argument('nprifile', help='Input NPRI File')
parser.add_argument('outdir', help='Output directory')
args = parser.parse_args()

args.nprifile = os.path.abspath(args.nprifile)
args.outdir = os.path.abspath(args.outdir)

fields = ['REP_PERIOD','NPRI_ID','COMP_NAME','FACI_NAME','LATI_DEC','LONG_DEC','CHEM_E','CAS_Number','UNITS_STOR','TOTAL_AIR','Total_kg']

agg = {
    'abcomm': 'Ab_id',
    'city': 'City_id',
    'ecozone': 'Eco_id',
    'health': 'HR_id',
    'prov': 'Prov_id',
    'wshed': 'WSHED'
}

header = {}
for x in agg.keys():
    header[x] = ['UniqueID', agg[x]] + fields

print "Splitting NPRI csv source {}".format(args.nprifile)

with open(args.nprifile, 'rb') as f:
    reader = csv.DictReader(f)
    progress = 1
    done = float(check_output(['wc', '-l', args.nprifile]).split()[0])
    aggregated_data_dict = defaultdict(set)
        # go through aggregation keys appending to appropriate data structre
    for line in reader:
        progress += 1
        sys.stdout.write("\r{:.2%}".format(progress/done))
        for k, v in agg.iteritems():
            if line[v]:
                if k == 'prov':
                    if line[v] == 'NL':
                        line[v] = 'NFLD'
                    elif line[v] == 'PE':
                        line[v] = 'PEI'
                    elif line[v] == 'NT':
                        line[v] = 'NWT'
                    elif line[v] == 'NU':
                        line[v] = 'NUN'
                outputline = tuple([line.get(x, '') for x in header[k]])
                aggregated_data_dict[k].add(outputline)
    print ' -- DONE PROCESSING FILE'

    for key in agg.keys():
        outdata = list(aggregated_data_dict[key])
        print key + ': ' + str(len(outdata))
        ensureDir(os.path.join(args.outdir, key))
        outfile = os.path.join(args.outdir, key,
            os.path.basename(args.nprifile).split('_')[0] + '_' + key + '_intermediate.csv')
        with open(outfile, 'wb') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(header[key])
            writer.writerows(outdata)
