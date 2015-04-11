#!/usr/bin/env python
#
# MakeH5: reads a CSV, makes a smaller dataframe based on a query using .loc, and then writes an H5 file
# GetSeries: loads the resulting file H5 file and gets the series to be plotted
# PlotSeries: displays a plot of the series
#
# TODO see below

# Key variables defined at start of main routineInput variables

import pandas, os
from faocodes import GetDictionary, QueryForProperties
from matplotlib import pyplot

global prop_dict

def MakeH5(item_code_list):
# reading this huge csv file is slow, but this will get the data for the regions I need and save it as an hdf5 file
    print "Reading h5 file..." 
    print 
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
    print "No. of Values Per Column"
    print "-----------------------------"
    results_list = []
    for column in df:
        temp_group = df.groupby(column)
        column_list = []
        column_list.append(column)
        column_list.append(len(temp_group))
        results_list.append(column_list)
    for result_pair in results_list: 
        print result_pair[0]+":", result_pair[1] 
    print

def GetCropLabel(bk_code):
    # First get the property dictionary
    prop_dict_list = QueryForProperties(str(bk_code), GetDictionary())
    # get the label from the right dictionary (there may be two of them)
    for dictionary in prop_dict_list:
        if "description" in dictionary: # i.e. if item is a crop and not a country
            crop_label = dictionary["label"]
    return crop_label

def PreviewDataByItem(df, item_code_list):
    print
    print "Preview of Data by Item"
    print "-----------------------------"
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

##### The following can be run as main routines ####

item_code_list = [254, 256, 257] # 258 and 259 were empty 
country_code_list = [101, 131, 5000] 

# narrow and convert the data, only need to do this once
# MakeH5(item_code_list)

# Read the file saved by MakeH5()        
df = pandas.read_hdf("E_select_crops.h5", 'data')

# A preview of the data which is most useful with the very large dataset before creating the h5 
#PreviewColumns(df)
# A comparison to decide which series to plot
#PreviewDataByItem(df, item_code_list)

# based on the output of the above, code 254 is what we want
oil_palm_df = df.loc[df["Item Code"].isin([254])]

# i'm not sure which element I want, let's check
for element in oil_palm_df.groupby("Element"):
    print element[0]
for element in oil_palm_df.groupby("Unit"):
    print element[0]

# "Production", I'm too lazy to get the code
prod_oil_palm_df = oil_palm_df.loc[df["Element"].isin(["Production"])]
#PreviewColumns(prod_oil_palm_df)

# check that our only unit is "tonnes"
for element in prod_oil_palm_df.groupby("Unit"):
    print element[0]

# make a country dict
for country in prod_oil_palm_df.groupby("Country"):
    print element[0]

for country_code in country_code_list:
    # narrow the frame temporarily to one country
    country_frame = prod_oil_palm_df.loc[df["Country Code"].isin([country_code])]
    # now we can index by year because there should only be one row per year
    country_frame = country_frame.set_index('Year')
    # make the series and check it
    country_series = pandas.Series(country_frame["Value"])
    PreviewColumns(country_series)
    # and put it in the plot
    pyplot.plot(country_series.index.values, country_series, marker = '.', label = country_code)

pyplot.title("Palm Oil Production 1961-2014")
pyplot.xlabel('Years')
pyplot.ylabel('Metric Tonnes')
pyplot.legend(loc='best')
pyplot.show()
