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
from faocodes import Code2Crop, Code2Country
import BW
from BW import set_ax_lines_bw, set_fig_lines_bw

global item_code_list
global element_code_list
global country_code_list
global input_CSV_filename
global H5_filename
 
input_CSV_filename = "QC.csv"
H5_filename = "QC_crops_selected.h5"

item_code_list = [254, 256, 257]                # 254 = "Oil, palm fruit", the others go in to the data file but not the chart
country_code_list = [131, 101]            # 101 = Indonesia; 131 = Malaysia
element_code_list = [5312]                      # 5312 = Production  

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
    print "Reading the H5 file..."
    df = pandas.read_hdf(H5_filename, 'data')
    print 
    print df.describe()
    print "Narrowing the data to", Code2Crop(item_code_list[0]) 
    item_df = df.loc[df["Item Code"].isin([item_code_list[0]])]
    print item_df.head()
    print "Narrowing the data to element", element_code_list[0]
    element_item_df = item_df.loc[df["Element Code"].isin(element_code_list)]
    print element_item_df.head()
    return element_item_df

def make_country_series(country_code, element_item_df):
    print "Creating a data series for", Code2Country(country_code)+"..."
    # make a temporary frame with just one country
    country_frame = element_item_df.loc[element_item_df["Country Code"].isin([country_code])]
    # this is narrow enough that we can index by year 
    country_frame = country_frame.set_index('Year')
    # now make the series of values
    country_series = pandas.Series(country_frame["Value"]/1000)
    print country_series.head(3)
    return country_series

def make_plot(ymax):
    image_file_name = "plot.png"
    # This part still needs to be automated
    pyplot.title("Palm Oil Production 1961-2013")
    pyplot.xlabel('Years')
    pyplot.ylabel('Metric Tonnes (thousands)')
    xmin = 1960
    xmax = 2015
    ymin = 0
    pyplot.xlim(xmin, xmax)
    pyplot.ylim(ymin, ymax)
    set_fig_lines_bw(pyplot.gcf())
    pyplot.legend(loc='best')
    pyplot.show()
    #print "Saving output to", image_file_name+"!"
    #pyplot.savefig(image_file_name)

def get_line_dict(element_item_df):
    series_dict = {}
    for country_code in country_code_list:
        # get country series, using country name as key - this will be a lot better when I make a Country class
        series_dict[(Code2Country(country_code))] = make_country_series(country_code, element_item_df)
    # make a line for "rest of world"
    world_series = make_country_series(5000, element_item_df)
    series_dict["Rest of World"] = world_series - (series_dict["Indonesia"] + series_dict["Malaysia"])
    return series_dict

if __name__ == '__main__':
    # 1) Haven't set up arguments yet
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    # 2) make the H5 file automatically if it does not already exist
    if not os.path.isfile(H5_filename):
        print H5_filename, "not found..."
        make_H5(item_code_list)
    # 3) Get the data frame from the file, with only the element code(s) we want
    element_item_df = make_df()
    # 4) make a dictionary, with each entry a line to plot
    series_dict = get_line_dict(element_item_df)
    # 5) plot each series in the dict 
    # for now "key" is a country name, etc.
    ymax = 0
    for key in series_dict:
        pyplot.plot(series_dict[key].index.values, series_dict[key], label = key)
        # increase ymax if needed
        for value in series_dict[key]:
            if value > ymax:
                ymax = value + (value * .01)
    # Format and display the thing
    make_plot(ymax)
