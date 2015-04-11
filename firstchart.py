import pandas, os

def MakeH5():
# reading this huge csv file is slow, but this will get the data for the regions I need and save it as an hdf5 file
    
    # read the csv
    csv_file_name = "E_production_crops_all.csv"
    print "Reading from file", csv_file_name, "..."
    raw_df = pandas.DataFrame.from_csv("E_production_crops_all.csv")
    
    # add an index column
    raw_df = raw_df.reset_index()

    #TODO write a dictionary to a json file based on "Country", "Item", "Element"
    #TODO drop those columns (and also "Year Code") from the df
    
    # check
    print raw_df.head(3)

    # narrow by Item Code
    # TODO interactively choose item codes, etc.
    item_code_list = [254, 256, 257, 258, 259]
    print "Narrowing the data..."
    narrow_df = raw_df.loc[raw_df["Item Code"].isin(item_code_list)]
    del raw_df
    print narrow_df.describe()

    # save to hdf5 and clear memory
    output = "production_crops_narrowed.h5"
    print "Saving to", output, "..."
    narrow_df.to_hdf(output, 'data', mode='w', format='fixed') 
    del narrow_df

# This one is not ready yet
def GetSeries():
    # Load the file 
    raw_df = pandas.read_hdf("production_crops_narrowed.h5",'data')
    # TODO narrow again by item
    # TODO create make the series
    # TODO plot the series

# narrow and convert the data, only need to do this once
# MakeH5()
        
# Test confirms that MakeH5 worked by reading the data
print "Reading h5 file..." 
df = pandas.read_hdf("production_crops_narrowed.h5", 'data')
print df.describe()
