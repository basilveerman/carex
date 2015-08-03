#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import glob
import csv
import argparse
import sys

from subprocess import check_output
from collections import defaultdict

from resources import ensureDir

parser = argparse.ArgumentParser(description='Split aggregation units')
parser.add_argument('indir', help='Input directory')
parser.add_argument('outdir', help='Output directory')
args = parser.parse_args()

args.indir = os.path.abspath(args.indir)
args.outdir = os.path.abspath(args.outdir)

fields = ['Buta_kg','Buta_TQ','Benz_kg','Benz_TQ','Form_kg','Form_TQ','Perc_kg','Perc_TQ','Chlor_kg','Chlor_TQ','Dichlor_kg','Dichlor_TQ','Acet_kg','Acet_TQ','PCB_kg','PCB_TQ','Ethylb_kg','Ethylb_TQ','Tcdd_kg','Tcdd_TQ','Ars_kg','Ars_TQ','Cadm_kg','Cadm_TQ','Hexcr_kg','Hexcr_TQ','Lead_kg','Lead_TQ','Nick_kg','Nick_TQ','BAA_kg','BAA_TQ','BBF_kg','BBF_TQ','BKF_kg','BKF_TQ','BAP_kg','BAP_TQ','Indeno_kg','Indeno_TQ','Chrys_kg','Chrys_TQ','Pm25_kg','PM25_TQ']

agg_col = {
    'abcomm': 'Ab_id',
    'city': 'City_id',
    'ecozone': 'Eco_id',
    'health': 'HR_id',
    'prov': 'Prov_id',
    'wshed': 'WSHED'
    }

header = {}
for k, v in agg_col.iteritems():
    header[k] = ['UniqueID', v] + fields

airports_with_duplicates = [
    {
        'agg_region': ['abcomm','city','ecozone','health','prov','wshed'],
        'infile': 'Airports_All.csv',
        'outfile': 'Airplanes taking off and landing'
    }
]

multi_sources = [
    {
        'agg_region': ['ecozone','health','prov','wshed'],
        'infile': 'GAS_All.csv',
        'outfile': 'Residential heating - Gas'
    },
    {
        'agg_region': ['ecozone','health','prov','wshed'],
        'infile': 'OIL_All.csv',
        'outfile': 'Residential heating - Oil'
    },
    {
        'agg_region': ['ecozone','health','prov','wshed'],
        'infile': 'WOOD_All.csv',
        'outfile': 'Residential heating - Wood'
    }
]

road_sources = [
    {
        'agg_region': 'abcomm',
        'infile': 'Roads_Ab_estimate.csv', 
        'agg_column': 'Ab_id', 
        'header': ['UniqueID', 'Abor_band'] + fields,
        'outfile': 'Vehicle traffic'
    },
    {
        'agg_region': 'city',
        'infile': 'Roads_City_estimate.csv', 
        'agg_column': 'City_id', 
        'header':['UniqueID', 'City_name'] + fields,
        'outfile': 'Vehicle traffic'
    },
    {
        'agg_region': 'ecozone',
        'infile': 'Roads_Eco_estimate.csv', 
        'agg_column': 'Eco_id', 
        'header':['UniqueID', 'Eco_id'] + fields,
        'outfile': 'Vehicle traffic'
    },
    {
        'agg_region': 'health',
        'infile': 'Roads_Health_estimate.csv', 
        'agg_column': 'HR_id', 
        'header':['UniqueID', 'HR_id'] + fields,
        'outfile': 'Vehicle traffic'
    },
    {
        'agg_region': 'prov',
        'infile': 'Roads_Prov_estimate.csv', 
        'agg_column': 'Prov_id', 
        'header':['UniqueID', 'Prov_id'] + fields,
        'outfile': 'Vehicle traffic'
    },
    {
        'agg_region': 'wshed',
        'infile': 'Roads_Shed_estimate.csv', 
        'agg_column': 'WSHED', 
        'header':['UniqueID', 'Shed_code'] + fields,
        'outfile': 'Vehicle traffic'
    }
]

rail_sources = [
    {
        'agg_region': 'abcomm',
        'infile': 'Rail_Ab_estimate.csv', 
        'agg_column': 'Ab_com_id', 
        'header': ['UniqueID', 'Abor_band'] + fields,
        'outfile': 'Rail transportation'
    },
    {
        'agg_region': 'city',
        'infile': 'Rail_City_estimate.csv', 
        'agg_column': 'City_id', 
        'header':['UniqueID', 'City_name'] + fields,
        'outfile': 'Rail transportation'
    },
    {
        'agg_region': 'ecozone',
        'infile': 'Rail_Eco_estimate.csv', 
        'agg_column': 'Eco_id', 
        'header':['UniqueID', 'Eco_id'] + fields,
        'outfile': 'Rail transportation'
    },
    {
        'agg_region': 'health',
        'infile': 'Rail_Health_estimate.csv', 
        'agg_column': 'HR_id', 
        'header':['UniqueID', 'HR_id'] + fields,
        'outfile': 'Rail transportation'
    },
    {
        'agg_region': 'prov',
        'infile': 'Rail_Prov_estimate.csv', 
        'agg_column': 'PROV', 
        'header':['UniqueID', 'Province'] + fields,
        'outfile': 'Rail transportation'
    },
    {
        'agg_region': 'wshed',
        'infile': 'Rail_Sheds_estimate.csv', 
        'agg_column': 'WSHED', 
        'header':['UniqueID', 'Shed_code'] + fields,
        'outfile': 'Rail transportation'
    }
]

city_abcom_sources = [
    #CITY
    {
        'agg_region': 'city',
        'infile': 'CITY_GAS.csv', 
        'agg_column': 'City_id', 
        'header': ['UniqueID', 'City_name'] + fields,
        'outfile': 'Residential heating - gas'
    },
    {
        'agg_region': 'city',
        'infile': 'CITY_OIL.csv', 
        'agg_column': 'City_id', 
        'header': ['UniqueID', 'City_name'] + fields,
        'outfile': 'Residential heating - Oil'
    },
    {
        'agg_region': 'city',
        'infile': 'CITY_WOOD.csv', 
        'agg_column': 'City_id', 
        'header': ['UniqueID', 'City_name'] + fields,
        'outfile': 'Residential heating - Wood'
    },

    #ABCOM
    {
        'agg_region': 'abcomm',
        'infile': 'ABCOM_GAS.csv', 
        'agg_column': 'Com_id', 
        'header': ['UniqueID', 'City_name'] + fields,
        'outfile': 'Residential heating - Gas'
    },
    {
        'agg_region': 'abcomm',
        'infile': 'ABCOM_OIL.csv', 
        'agg_column': 'Com_id', 
        'header': ['UniqueID', 'City_name'] + fields,
        'outfile': 'Residential heating - Oil'
    },
    {
        'agg_region': 'abcomm',
        'infile': 'ABCOM_WOOD.csv', 
        'agg_column': 'Com_id', 
        'header': ['UniqueID', 'City_name'] + fields,
        'outfile': 'Residential heating - Wood'
    }
]

def process_source(k, v):
    infile = os.path.join(args.indir, v['infile'])
    outfile = os.path.join(args.outdir, k, v['outfile'] + '.csv')
    print infile
    with open(infile, 'rb') as f_in:
        reader = csv.DictReader(f_in)
        with open(outfile, 'wb') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(v['header'])
            col = v['agg_column']
            for line in reader:
                if k == 'prov':
                    if line[col] == 'NL':
                        line[col] = 'NFLD'
                    elif line[col] == 'PE':
                        line[col] = 'PEI'
                    elif line[col] == 'NT':
                        line[col] = 'NWT'
                    elif line[col] == 'NU':
                        line[col] = 'NUN'
                    elif line[col] == 'QC':
                        line[col] = 'PQ'
                    elif line[col] == 'YT':
                        line[col] = 'YK'

                if k == 'city':
                    if line[col].decode('utf-8') == u'Montr?al':
                        line[col] = 'Montreal'
                    elif line[col].decode('utf-8') == u'Qu?bec':
                        line[col] = 'Quebec'
                    elif line[col].decode('utf-8') == u'Trois-Rivi?res':
                        line[col] = 'Trois-Rivieres'
                    elif line[col].decode('utf-8') == u'Jonqui?re':
                        line[col] = 'Jonquiere'
                    elif line[col].decode('utf-8') == u'MontrΘal':
                        line[col] = 'Montreal'
                    elif line[col].decode('utf-8') == u'QuΘbec':
                        line[col] = 'Quebec'
                    elif line[col].decode('utf-8') == u'Trois-RiviΦres':
                        line[col] = 'Trois-Rivieres'
                    elif line[col].decode('utf-8') == u'JonquiΦre':
                        line[col] = 'Jonquiere'
                
                # print line
                outline = [line[x] if x!='UniqueID' else '' for x in ['UniqueID', v['agg_column']] + fields] 
                writer.writerow(outline)

def process_multiple_trim_duplicates(prefs):
    print prefs['infile']
    infile = os.path.join(args.indir, prefs['infile'])
    with open(infile, 'rb') as f:
        reader = csv.DictReader(f)
        progress = 1
        done = float(check_output(['wc', '-l', infile]).split()[0])
        aggregated_data_dict = defaultdict(set)

        # go through aggregation keys appending to appropriate data structre
        for line in reader:
            progress += 1
            sys.stdout.write("\r{:.2%}".format(progress/done))
            for agg_region in prefs['agg_region']:
                k = agg_col[agg_region]
                if line[k]:

                    # do some on the fly corrections
                    if agg_region == 'prov':
                        if line[k] == 'NL':
                            line[k] = 'NFLD'
                        elif line[k] == 'PE':
                            line[k] = 'PEI'
                        elif line[k] == 'NT':
                            line[k] = 'NWT'
                        elif line[k] == 'NU':
                            line[k] = 'NUN'
                        elif line[k] == 'QC':
                            line[k] = 'PQ'
                        elif line[k] == 'YT':
                            line[k] = 'YK'

                    # city corrections
                    if agg_region == 'city':
                        if line[k].decode('utf-8') == u'Montr?al':
                            line[k] = 'Montreal'
                        elif line[k].decode('utf-8') == u'Qu?bec':
                            line[k] = 'Quebec'
                        elif line[k].decode('utf-8') == u'Trois-Rivi?res':
                            line[k] = 'Trois-Rivieres'
                        elif line[k].decode('utf-8') == u'Jonqui?re':
                            line[k] = 'Jonquiere'
                        elif line[k].decode('utf-8') == u'MontrΘal':
                            line[k] = 'Montreal'
                        elif line[k].decode('utf-8') == u'QuΘbec':
                            line[k] = 'Quebec'
                        elif line[k].decode('utf-8') == u'Trois-RiviΦres':
                            line[k] = 'Trois-Rivieres'
                        elif line[k].decode('utf-8') == u'JonquiΦre':
                            line[k] = 'Jonquiere'

                    outputline = tuple([line.get(x, '') for x in header[agg_region]])
                    aggregated_data_dict[agg_region].add(outputline)
    print ' -- DONE PROCESSING FILE'

    for agg_region in prefs['agg_region']:
        outdata = list(aggregated_data_dict[agg_region])
        print agg_region + ': ' + str(len(outdata))
        ensureDir(os.path.join(args.outdir, agg_region))
        outfile = os.path.join(args.outdir, agg_region, prefs['outfile'] + '.csv')
        with open(outfile, 'wb') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(header[agg_region])
            writer.writerows(outdata)

def process_multiple(prefs):
    print prefs['infile']
    infile = os.path.join(args.indir, prefs['infile'])
    with open(infile, 'rb') as f:
        reader = csv.DictReader(f)
        progress = 1
        done = float(check_output(['wc', '-l', infile]).split()[0])
        aggregated_data_dict = defaultdict(list)

        # go through aggregation keys appending to appropriate data structre
        for line in reader:
            progress += 1
            sys.stdout.write("\r{:.2%}".format(progress/done))
            for agg_region in prefs['agg_region']:
                k = agg_col[agg_region]
                if line[k]:

                    # do some on the fly corrections
                    if agg_region == 'prov':
                        if line[k] == 'NL':
                            line[k] = 'NFLD'
                        elif line[k] == 'PE':
                            line[k] = 'PEI'
                        elif line[k] == 'NT':
                            line[k] = 'NWT'
                        elif line[k] == 'NU':
                            line[k] = 'NUN'
                        elif line[k] == 'QC':
                            line[k] = 'PQ'
                        elif line[k] == 'YT':
                            line[k] = 'YK'

                    # city corrections
                    if agg_region == 'city':
                        if line[k].decode('utf-8') == u'Montr?al':
                            line[k] = 'Montreal'
                        elif line[k].decode('utf-8') == u'Qu?bec':
                            line[k] = 'Quebec'
                        elif line[k].decode('utf-8') == u'Trois-Rivi?res':
                            line[k] = 'Trois-Rivieres'
                        elif line[k].decode('utf-8') == u'Jonqui?re':
                            line[k] = 'Jonquiere'
                        elif line[k].decode('utf-8') == u'MontrΘal':
                            line[k] = 'Montreal'
                        elif line[k].decode('utf-8') == u'QuΘbec':
                            line[k] = 'Quebec'
                        elif line[k].decode('utf-8') == u'Trois-RiviΦres':
                            line[k] = 'Trois-Rivieres'
                        elif line[k].decode('utf-8') == u'JonquiΦre':
                            line[k] = 'Jonquiere'

                    outputline = [line.get(x, '') for x in header[agg_region]]
                    aggregated_data_dict[agg_region].append(outputline)
    print ' -- DONE PROCESSING FILE'

    for agg_region in prefs['agg_region']:
        outdata = aggregated_data_dict[agg_region]
        print agg_region + ': ' + str(len(outdata))
        ensureDir(os.path.join(args.outdir, agg_region))
        outfile = os.path.join(args.outdir, agg_region, prefs['outfile'] + '.csv')
        with open(outfile, 'wb') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(header[agg_region])
            writer.writerows(outdata)

print "Reformatting sources in {}".format(args.indir)

print "ROADS"
for entry in road_sources:
    process_source(entry['agg_region'], entry)

print "RAILS"
for entry in rail_sources:
    process_source(entry['agg_region'], entry)

print "Airports"
for entry in airports_with_duplicates:
    process_multiple_trim_duplicates(entry)

print "Multi-aggregate file"
for entry in multi_sources:
    process_multiple(entry)

print "CITY and ABCOM"
for entry in city_abcom_sources:
    process_source(entry['agg_region'], entry)
