#!/usr/bin/python 
#
# script to make a simple plot of a csv file

import argparse
import os
import pandas
import matplotlib
from matplotlib import pyplot

def csv2plot(csv_filename):
    df = pandas.DataFrame.from_csv(args.filename)
    for column in df:
        pyplot.plot(df[column].index.values, df[column], label=column)
    pyplot.xlabel(df.index.name)
    pyplot.title(os.path.split(args.filename)[1])
    pyplot.legend(loc='best')
    pyplot.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='make a quick plot from a csv file')
    parser.add_argument('filename', help='csv file to be plotted')
    args = parser.parse_args()
    csv_filename = args.filename
    csv2plot(csv_filename)
