# Main routine asks user for a search string, then prints a list of FAOSTAT country and/or item codes for any matches.
#
# data is read from members.json, which can be downloaded directly at: 
# http://data.fao.org/developers/api/v1/en/resources/members.json?page=1&pageSize=1000&fields=mnemonic%2Clabel%40en%2Cproperties.*
#
# Search is case insensitive. The detailed "description" property is included in the search, so unexpected results are common. 

import json

def FaostatGetDictionary():
    # loads the main dictionary from members.json
    prop_dict = {}
    temp_list = []
    with open("members.json", 'r') as data_file:
        raw_data = json.load(data_file)    
    for item in raw_data["result"]["list"]["items"]:
        prop_dict[item["label"]] = item["properties"]
        temp_list.append(item["properties"])
    return prop_dict

def FaostatCodeQuery(search_string, prop_dict):
    # gets labels and codes from the dictionary based on a simple string search
    pair_list = [] 
    for key in prop_dict:
        label = prop_dict[key]["label"]
        code = prop_dict[key]["bk"]
        if search_string.lower() in str(prop_dict[key]).lower():
            result = [label, code]
            pair_list.append(result)
    return pair_list


if __name__ == '__main__':
    prop_dict = FaostatGetDictionary()
    search_string = raw_input("Enter your search string: ")
    code_list = FaostatCodeQuery(search_string, prop_dict)
    code_list = sorted(code_list)
    print ""
    for result in code_list:
        if len(result[0]) < 7:
            print result[0],"\t", "\t", "\t", "\t", "\t", result[1]
        elif len(result[0]) < 15:
            print result[0],"\t", "\t", "\t", "\t", result[1]
        elif len(result[0]) < 23:
            print result[0],"\t", "\t", "\t", result[1]
        elif len(result[0]) < 30:
            print result[0],"\t", "\t", result[1]
        else:
            print result[0],"\t", result[1]
