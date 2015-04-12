def preview_columns(df):
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

def preview_by_item(df, item_code_list):
    print
    print "Preview of Data by Item"
    print "-----------------------------"
    for item_code in item_code_list:
        temp_df = df.loc[df["Item Code"].isin([item_code])]
        print
        print "Item Code", item_code, "("+GetCropLabel(item_code)+")", "..."
        print 
        print temp_df.describe()
