#!/usr/bin/env python
#
# MakeH5: reads a CSV, makes a smaller dataframe based on a query using .loc, and then writes an H5 file
# GetSeries: loads the resulting file H5 file and gets the series to be plotted
# PlotSeries: displays a plot of the series
#
# TODO see below

# Input variables
item_code_list = [254, 256, 257] # 258 and 259 were empty 

import pandas, os
from faocodes import GetDictionary, QueryForProperties

global prop_dict

def MakeH5(item_code_list):
# reading this huge csv file is slow, but this will get the data for the regions I need and save it as an hdf5 file
    # read the csv
    csv_file_name = "E_production_crops_all.csv"
    print "Reading from file", csv_file_name, "..."
    raw_df = pandas.DataFrame.from_csv("E_production_crops_all.csv")
    # add an index column
    raw_df = raw_df.reset_index()
    #TODO write a dictionary to a json file based on "Country", "Item", "Element"
    #TODO delete those columns (and also "Year Code") from the df
    # Quick check of data
    print raw_df.head(3)
# Done reading data, now narrow it by Item Code
    # TODO interactively choose item codes, etc.
    print "Narrowing the data..."
    narrow_df = raw_df.loc[raw_df["Item Code"].isin(item_code_list)]
    del raw_df
    print narrow_df.describe()

    # save to hdf5 and clear memory
    output = "E_select_crops.h5"
    print "Saving to", output, "..."
    narrow_df.to_hdf(output, 'data', mode='w', format='fixed') 
    del narrow_df

def PreviewColumns(df):
    results_list = []
    for column in df:
        temp_group = df.groupby(column)
        column_list = []
        column_list.append(column)
        column_list.append(len(temp_group))
        results_list.append(column_list)
    for result_pair in results_list: 
        print result_pair[0]+":", result_pair[1] 

def GetCropLabel(bk_code):
    # First get the property dictionary
    prop_dict_list = QueryForProperties(str(bk_code), GetDictionary())
    # get the label from the right dictionary (there may be two of them)
    for dictionary in prop_dict_list:
        if "description" in dictionary: # i.e. if item is a crop and not a country
            crop_label = dictionary["label"]
    return crop_label

def PreviewDataByItem(df, item_code_list):
    # Get the series for each items
    for item_code in item_code_list:
        temp_df = df.loc[df["Item Code"].isin([item_code])]
        print
        print "Item Code", item_code, "("+GetCropLabel(item_code)+")", "..."
        print 
        print temp_df.describe()

#def GetSeries(df, item_code):
    # TODO narrow again by item
    # TODO create make the series
    # TODO plot the series

# The following can be run as main routines 

# narrow and convert the data, only need to do this once
# MakeH5(item_code_list)

# Read the file saved by MakeH5()        
print "Reading h5 file..." 
print 
df = pandas.read_hdf("E_select_crops.h5", 'data')

# A preview of the data which is most useful with the very large dataset before creating the h5 
print "No. of Values Per Column"
print "-----------------------------"
PreviewColumns(df)

# A comparison to decide which series to plot
print "Preview of Data by Item"
print "-----------------------------"
PreviewDataByItem(df, item_code_list)

# this will come next
#for country in country_code_list:
#    country_series = GetSeries(df, country)
