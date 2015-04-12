#!/usr/bin/python 
# 
# 1) Takes lists of selected country, item, and element codes.
#  
# 2) If no H5 file exists, makes one by (slowly) reading from the FAOSTAT 
# csv datafile provided.  
#
# 3) Generates a plot showing all countries, based on the first item and 
# first element on this list. At the moment, titles need to be coded by hand.
# 
# 4) TODO Generate multiple plots with various item / element / country
# combinations 
# 
# TODO need to find or make a dictionary to look up Element from Element Code
# TODO make make_plot() more flexible

import argparse 
import os
import pandas
import matplotlib
from matplotlib import pyplot
import faocodes
from faocodes import Code2Crop, Code2Country

global item_code_list
global element_code_list
global country_code_list
global input_CSV_filename
global H5_filename
 
item_code_list = [254, 256, 257]                # 254 = "Oil, palm fruit", the others go in to the data file but not the chart
country_code_list = [101, 131]            # 101 = Indon.; 131 = Malaysia
input_CSV_filename = "E_production_crops_all.csv"
H5_filename = "E_select_crops.h5"

# this one is a string for now only because I don't have a dictionary 
# for the codes yet
element_to_plot = "Production" 

# Reading a huge csv file is very slow. This will get the data for 
# the regions I need, and save it as an hdf5 file. 
#
# Steps: 1) read the CSV file, 2) remove extra data, 3) save the new file 
def make_H5(item_code_list):
    # 1)
    print "Reading from file", csv_file_name, "..."
    raw_df = pandas.DataFrame.from_csv(input_CSV_filename)
    # This data doesn't have an index column, so add one
    raw_df = raw_df.reset_index()
    # 2)
    print "Narrowing the data..."
    # TODO should drop Element once we have a dictionary for it
    # for now, get rid of other strings and extra data
    raw_df.drop("Country", "Item", "Year Code")
    # key step here, cuts most of the data out
    narrow_df = raw_df.loc[raw_df["Item Code"].isin(item_code_list)]
    del raw_df
    # 3) 
    output = "E_select_crops.h5"
    print "Saving to", output, "..."
    narrow_df.to_hdf(output, 'data', mode='w', format='fixed') 
    del narrow_df

def make_df():
    # Read the H5 file.
    df = pandas.read_hdf(H5_filename, 'data')
    # Narrow the data down further to what we want to plot.
    item_df = df.loc[df["Item Code"].isin([item_code_list[0]])]
    element_item_df = item_df.loc[df["Element"].isin([element_to_plot])]
    return element_item_df

def make_country_series(country, element_item_df):
    # make a temporary frame with just one country
    country_frame = element_item_df.loc[element_item_df["Country Code"].isin([country_code])]
    # this is narrow enough that we can index by year 
    country_frame = country_frame.set_index('Year')
    # now make the series of values
    country_series = pandas.Series(country_frame["Value"]/1000000)
    return country_series

def make_plot():
    # This part still needs to be automated
    pyplot.title("Palm Oil Production 1961-2013")
    pyplot.xlabel('Years')
    pyplot.ylabel('Metric Tonnes (Millions)')
    pyplot.legend(loc='best')
    xmin = 1960
    xmax = 2014
    ymin = 0
    ymax = 125
    pyplot.xlim(xmin, xmax)
    pyplot.ylim(ymin, ymax)
    pyplot.show()
    pyplot.savefig("firstchart.png")

if __name__ == '__main__':
    # 1) Haven't set up arguments yet
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    # 2) make the H5 file automatically if it does not already exist
    if not os.path.isfile(H5_filename):
        make_H5(item_code_list)
    # 3) Get the data frame we want from the file
    element_item_df = make_df()
    # 4) Get the series from the dataframe for each country and plot it
    for country_code in country_code_list:
        # get country series
        country_series = make_country_series(country_code, element_item_df)
        # add it to the plot
        pyplot.plot(country_series.index.values, country_series, marker = '.', label = Code2Country(country_code))
    # Format and display the thing
    make_plot()
