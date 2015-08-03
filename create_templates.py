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
parser.add_argument('indir', help='Input directory')
parser.add_argument('outdir', help='Output directory')
args = parser.parse_args()

args.indir = os.path.abspath(args.indir)
args.outdir = os.path.abspath(args.outdir)

fields = ['Buta_kg','Buta_TQ','Benz_kg','Benz_TQ','Form_kg','Form_TQ','Perc_kg','Perc_TQ','Chlor_kg','Chlor_TQ','Dichlor_kg','Dichlor_TQ','Acet_kg','Acet_TQ','PCB_kg','PCB_TQ','Ethylb_kg','Ethylb_TQ','Tcdd_kg','Tcdd_TQ','Ars_kg','Ars_TQ','Cadm_kg','Cadm_TQ','Hexcr_kg','Hexcr_TQ','Lead_kg','Lead_TQ','Nick_kg','Nick_TQ','BAA_kg','BAA_TQ','BBF_kg','BBF_TQ','BKF_kg','BKF_TQ','BAP_kg','BAP_TQ','Indeno_kg','Indeno_TQ','Chrys_kg','Chrys_TQ','Pm25_kg','PM25_TQ']

agg = {
    'abcomm': 'Band_name',
    'city': 'City_name',
    'ecozone': 'Eco_id',
    'health': 'HR_id',
    'prov': 'Prov_id',
    'wshed': 'WSHED'
}

header = {}
for x in agg.keys():
    header[x] = ['UniqueID', agg[x]] + fields

print "Creating templates based on population files in {}".format(args.indir)

for key in agg.keys():
    agg_ids = []
    with open(os.path.join(args.indir, key + '_pop.txt'), 'rb') as f, open(os.path.join(args.outdir, key, 'population.txt'), 'wb') as pop_out:
        print f.name
        pop_out.writelines(f.readlines())
        f.seek(0)
        reader = csv.reader(f)
        reader.next() #skip header
        for line in reader:
            agg_ids.append(['',line[0]])

    ensureDir(os.path.join(args.outdir, key))
    outfile = os.path.join(args.outdir, key, 'template.txt')
    with open(outfile, 'wb') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header[key])
        writer.writerows(agg_ids)
