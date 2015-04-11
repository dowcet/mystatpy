#!/usr/bin/env python
# Main routine asks user for a search string, then prints a list of FAOSTAT country and/or item codes for any matches.
#
# data is read from members.json, which can be downloaded directly at: 
# http://data.fao.org/developers/api/v1/en/resources/members.json?page=1&pageSize=1000&fields=mnemonic%2Clabel%40en%2Cproperties.*
#
# Search is case insensitive. The detailed "description" property is included in the search, so unexpected results are common.
# 
# TODO Take input as an argument

import os, json, urllib

# this __location__ trick is from http://stackoverflow.com/questions/4060221/how-to-reliably-open-a-file-in-the-same-directory-as-a-python-script

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def GetDictionary():
    # loads the main dictionary from members.json
    # it contains a dictionary of property for every country and crop in FAOSTAT dataset "E"
    prop_dict = {}
    temp_list = []
    with open((os.path.join(__location__, "members.json")), 'r') as data_file:
        raw_data = json.load(data_file)    
    for item in raw_data["result"]["list"]["items"]:
        prop_dict[item["label"]] = item["properties"]
        temp_list.append(item["properties"])
    return prop_dict

def Code2Crop(bk_code):
# Gets the crop label to match a crop code
    # First get any property dictionary matching the code
    prop_dict_list = QueryForProperties(str(bk_code), GetDictionary())
    # if there is a dictionary for a crop, get the label 
    for dictionary in prop_dict_list:
        if "description" in dictionary: # i.e. if item is a crop and not a country
            crop_label = dictionary["label"]
    return crop_label

def Code2Country(bk_code):
# Gets the country label to match a country code
    # First get any property dictionary matching the code
    prop_dict_list = QueryForProperties(str(bk_code), GetDictionary())
    # if there is a dictionary for a country, get the label 
    for dictionary in prop_dict_list:
        if not "description" in dictionary: # i.e. if item is not a crop, and therefore a country
            country_label = dictionary["label"]
    return country_label
    

def QueryForProperties(code, prop_dict):
    # gets the properties for any member(s) matching the numerical code
    results_list = []
    for key in prop_dict:
        if int(prop_dict[key]["bk"]) == int(code):
            results_list.append(prop_dict[key])
    return results_list

def QueryForCodes(search_string, prop_dict):
    # gets a list of codes and labels based on a search string 
    pair_list = [] 
    for key in prop_dict:
        label = prop_dict[key]["label"]
        code = prop_dict[key]["bk"]
        if search_string.lower() in str(prop_dict[key]).lower():
            result = [label, code]
            pair_list.append(result)
    return pair_list

def OutputProperties(code, results_list):
    if not results_list:
        print
        print "No matches found for code", code
    else:
        for result in results_list:
            # clean up the label
            label = result["label"]
            label = label.replace("&apos;", "'")
            label = label.replace("&amp;", "&")
            if "description" in result:
                # clean up the description
                descrip = result["description"]
                descrip = descrip.replace("&apos;", "'")
                descrip = descrip.replace("&amp;", "&")
                # and now the output
                print
                print "Item", code+":" 
                print label
                print
                print "Description: ", descrip
            else:
                print
                print "Region", code+":"
                print label

def OutputCodeList(code_list):
    print "\n"
    for result in code_list:
        label = result[0]
        label = label.replace("&amp;", "&")
        label = label.replace("&apos;", "'")
        code = str(result[1])
        if len(label) < 8:
            output_line = label+"\t------------------------------- "+code
        elif len(label) < 16:
            output_line =  label+"\t----------------------- "+code
        elif len(label) < 24:
            output_line =  label+"\t--------------- "+code
        elif len(label) < 32:
            output_line =  label+"\t\t"+code
        else:
            output_line = label+"\t"+code
        print output_line

if __name__ == '__main__':
    search_string = raw_input("Enter your search string or numerical code: ")
    prop_dict = GetDictionary()
    if search_string.isdigit():
        properties_list = QueryForProperties(search_string, prop_dict)
        OutputProperties(search_string, properties_list)
    else:
        code_list = sorted(QueryForCodes(search_string, prop_dict))
        OutputCodeList(code_list)
