import pandas, os

def MakeH5():
    # reading this huge csv file is slow, but this will get the data for the regions I need and save it as an hdf5 file
    #
    # 1) read the csv
    raw_df = pandas.DataFrame.from_csv("E_production_crops_all.csv")
    #
    # 2) filter by country
    narrowed = raw_df.loc[raw_df["Country"].isin(["Malaysia", "Indonesia", "World"])]
    #
    # 3) save to hdf5 and clear memory
    output = "narrowed.h5"
    narrowed.to_hdf(output, 'data', mode='w', format='fixed') 
    del raw_df

# This one is not ready yet
def GetSeries():
    # Load the file 
    df = pandas.read_hdf("narrowed.h5", 'data')
    # TODO now 
    
# Test confirms that MakeH5 worked by reading the data
df = pandas.read_hdf("narrowed.h5", 'data')
print df.head   

