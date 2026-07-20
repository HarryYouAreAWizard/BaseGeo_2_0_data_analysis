

"""
file: viable_questions_filtering.py
author: Noah Nielsen
date: 2026-04-18
This module provides functions for filtering survey 
questions based on their viability for analysis.
"""


def get_scale(question, dataframe):
    """get a prototype of the scale of a question in a dataframe
    
    This function is related to the detect_axis function in axis.py. However, 
    this one just finds which names are being used, but does not match anything
    """
    return dataframe[question].dropna().unique()

def clean_scale_entries(scale_entries):
    """keep only the entries that can be converted to numbers, and sort them"""
    return sorted([entry for entry in scale_entries if entry[0].isdigit()])
    
def is_ambiguous_scale(scale_entries):
    """
    check if multiple instances of 1 and 7 have different text
    """
    for entry in scale_entries:
        # early exit. only 1 and 7 actually differ
        if entry[0] not in ["1", "7"]:
            continue

        # if entry[0] == "7":
        for other_entry in scale_entries:
            # check that they are the same category 
            if entry[0] != other_entry[0]:
                continue

            # check if they are exactly the same, if so, skip
            if other_entry.strip() == entry.strip():
                continue

            print(f"Ambiguous scale detected: {entry} and {other_entry}, {entry == other_entry}")
            return True
                
        # elif entry[0] == "1":
        #     for other_entry in scale_entries:
        #         if other_entry.strip() == entry.strip():
        #             continue
        #         if other_entry[0] == "1":
        #             print(f"Ambiguous scale detected: {entry} and {other_entry}, {entry == other_entry}")
        #             return True
                

    return False


