import numpy as np
import networkx as nx


# New function to return each dictionary that exist in
# the main dictionary of the network which matches
# the names of standard dictionaries that exist in a separate list
#  and then this function returns only a dictionary that include  all the other dictionaries.
# that match the names of items in the given list
# other way, it will raise an error
def create_specific_dict(main_dict, item_list):
    specific_dicts = {}
    for key, value in main_dict.items():
        if key in item_list:
            specific_dicts[key] = value
        else:
            print(
                "The names of all dictionaries of the main dictionary in the network don't match the standard names of dictionaries"
            )
    return specific_dicts


# a function to convert Nan into 1 for the checking if all nodes
# (except inputs) have at least one incoming positive edge so Nan can't be Zero
def convert_Nan_to_1(numpy_array):
    return np.where(np.isnan(numpy_array), 1, numpy_array)

