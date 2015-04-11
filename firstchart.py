#!/usr/bin/python 
# 
# TODO find or make a dictionary to look up Element from Element Code

import argparse 
import os
import pandas
import matplotlib
from matplotlib import pyplot
import faocodes
from faocodes import Code2Crop, Code2Country

global input_CSV_filename
global H5_filename
global item_code_list
global country_code_list
 
input_CSV_filename = "E_production_crops_all.csv"
H5_filename = "E_select_crops.h5"
item_code_list = [254, 256, 257]
country_code_list = [101, 131, 5000]
item_to_plot = 254
# this one is a string for now only because I don't have a dictionary 
# for the codes yet
element_to_plot = "Production" 

# Reading a huge csv file is very slow. This will get the data for 
# the regions I need, and save it as an hdf5 file. 
#
# 1) Read the CSV file, 2) Remove extra data, 3) Save the new file 
def makeH5(item_code_list):
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

if __name__ == '__main__':
    # I'm not actually sure I'll use arguments, but I'll leave them   
    # here for now
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # If it does not exist yet, make the H5 file automatically.
    if not os.path.isfile(H5_filename):
        makeH5(item_code_list)
    # Read the H5 file.
    df = pandas.read_hdf(H5_filename, 'data')

    # Narrow the data down further to what we want to plot.
    item_df = df.loc[df["Item Code"].isin([item_to_plot])]
    element_item_df = item_df.loc[df["Element"].isin([element_to_plot])]
 
    # Plot a series for each country
    for country_code in country_code_list:
        # Narrow the frame temporarily to just one country
        country_frame = element_item_df.loc[df["Country Code"].isin([country_code])]
        # Now we can index by year because there should only be one 
        # row per year
        country_frame = country_frame.set_index('Year')
        # Make the value series
        country_series = pandas.Series(country_frame["Value"])
        # put it in the plot
        pyplot.plot(country_series.index.values, country_series, marker = '.', label = Code2Country(country_code))

    # Format and display the thing
    pyplot.title("Palm Oil Production 1961-2013")
    pyplot.xlabel('Years')
    pyplot.ylabel('Metric Tonnes')
    pyplot.legend(loc='best')
    pyplot.show()
    pyplot.savefig("firstchart.png")
