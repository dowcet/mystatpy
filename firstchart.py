import pandas, os

def FirstRead():
    # reading this huge csv file is slow, this will get the data for the regions I need and save it as a hdf5 file
    #
    # read the csv
    raw_df = pandas.DataFrame.from_csv("~/dissertation/stats/downloads/faostat/E_production_crops_all.csv")
    #
    # filter by country
    filtered = raw_df.loc[raw_df["Country"].isin(["Malaysia", "Indonesia", "World"])]
    #
    # save to hdf5
    output = os.getcwd()+"mydata.h5"
    raw_df.to_hdf(output, 'data', mode='w', format='fixed') 
    del raw_df
