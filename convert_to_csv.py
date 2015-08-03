#!/usr/bin/python

import os
import glob
import argparse

from xlsx2csv import xlsx2csv

parser = argparse.ArgumentParser(description='Process some excel files to csv.')
parser.add_argument('indir', help='Input directory')
parser.add_argument('outdir', help='Output directory')
args = parser.parse_args()

if not os.path.exists(args.outdir): raise Exception
args.indir = os.path.abspath(args.indir)
args.outdir = os.path.abspath(args.outdir)

print "Looking for excel files in {}".format(args.indir)
for fpath in glob.glob(os.path.join(args.indir, '*.xlsx')):
    outfile = os.path.join(args.outdir, os.path.splitext(os.path.basename(fpath))[0] + '.csv')
    with open(outfile, 'wb') as f:
        try:
            print 'Processing {}'.format(os.path.basename(fpath))
            xlsx2csv(fpath, f, None)
            print '\t\t...Success!'
        except Exception as e:
            print e
            print '\t\t..Failed'
            continue
