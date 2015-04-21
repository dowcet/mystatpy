#!/usr/bin/python 
#
# script to make a simple plot of a csv file

import argparse
import os
import pandas
import matplotlib
from matplotlib import pyplot

def plot_csv(csv_filename):
    pyplot.clf()
    df = pandas.DataFrame.from_csv(csv_filename)
    for column in df:
        pyplot.plot(df[column].index.values, df[column], label=column)
    pyplot.xlabel(df.index.name)
    pyplot.title(os.path.split(csv_filename)[1])
    pyplot.legend(loc='best')
    pyplot.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description='make a quick plot from a csv file')
    parser.add_argument('filename', nargs='?', help='csv file to be plotted')
    args = parser.parse_args()
    if args.filename == None:
        csv_filename = raw_input("Enter CSV filename: ")
    else:
        csv_filename = args.filename
    plot_csv(csv_filename)
