import pandas, os

def MakeH5():
# reading this huge csv file is slow, but this will get the data for the regions I need and save it as an hdf5 file
    
    # read the csv
    raw_df = pandas.DataFrame.from_csv("E_production_crops_all.csv")
    
    # add an index column
    raw_df = raw_df.reset_index()
    
    # filter by country
    country_list = ["Malaysia", "Indonesia", "World"]
    narrowed = raw_df.loc[raw_df["Country"].isin(country_list)]
    
    # save to hdf5 and clear memory
    output = "narrowed.h5"
    narrowed.to_hdf(output, 'data', mode='w', format='fixed') 
    del raw_df

# This one is not ready yet
def GetSeries():
    # Load the file 
    raw_df = pandas.read_hdf("narrowed.h5",'data')
    # TODO narrow again by item
    # TODO create make the series
    # TODO plot the series
        
# Test confirms that MakeH5 worked by reading the data
df = pandas.read_hdf("narrowed.h5", 'data')
