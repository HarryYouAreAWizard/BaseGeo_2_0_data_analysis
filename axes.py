#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: axes.py
Author: Noah Nielsen
Created: 2026-04-18
Description: This module provides functions for normalizing survey responses, 
detecting which axis they belong to, and extracting counts for each response 
category. It handles various formats of survey responses and maps them to predefined axes for analysis.
"""

import pandas as pd
import re
from axes_container import AXES

UNIVERSAL_OPTIONS = [
    "Not applicable",
    "No idea",
    "I don't know",
    "I don&#39;t know",
]

def normalize_answer(value):
    """
    Normalize a string answer by stripping whitespace and collapsing multiple spaces.
    Returns None for empty or NaN values.
    """
    if pd.isna(value):
        return None

    text = str(value).strip()
    if not text:
        return None
    
    text = re.sub(r"\s+", " ", text)   # collapse repeated spaces
    
    return text

def detect_axis(values):
    """
    Detect which axis a set of values belongs to, based on the predefined AXES.

    returns botht the clean and the raw detected axis

    Returns the axis name, the labels for that axis, and any unmatched labels.
     - If exactly one axis matches, returns that axis and its labels.
     - If no axes match, returns "unknown" and the unique normalized labels.
     - If multiple axes match (should not happen if axes are disjoint), returns "ambiguous".

    This function fails to detect it, if there are multiple fits

    """
    # clean and normalize the input values to get a set of unique labels
    labels = {normalize_answer(v) for v in values}
    labels.discard(None)

    # check which axis match the labels, by running through all axis types and variants
    for axis_type in AXES.keys(): # frequency, importance, extent ...
        for axis_variation, axis_labels in AXES[axis_type].items(): # clean, with doubt, with typo ...

            # assemble a set of allowed labels for this specific acis variation
            allowed = set(axis_labels) or set(UNIVERSAL_OPTIONS)

            # check is the responses form a subset of the allowed labels for this axis variation
            if 0 and labels.issubset(allowed): 
                # this function is suspected to be incorrect
                axis = axis_type, AXES[axis_type][axis_type] # pick clean version
                return axis
            
            # if above fails try seeing if the first option from the clean axis is present in the responses (1. Strongly disagree, 1. Extremely little ...)
            if axis_labels[0] in labels:
                axis = axis_type, AXES[axis_type][axis_type] # pick clean version
                return axis
            
            # If above fails, try seeing if the last option from the clean axis is present in the responses (7. Strongly agree, 7. Extremely well ...)                
            if AXES[axis_type][axis_type][-1] in labels:
                axis = axis_type, AXES[axis_type][axis_type] # pick clean version
                return axis
            
            # if "7. Extremely welll" in labels:
            #     print("Edge case")
            #     axis = axis_type, AXES[axis_type][axis_type] # pick clean version
            #     return axis
            
    # not all questions have well defined axes
    return None

def extract_counts(values):
    """
    Given a list of raw values, normalize them and detect which axis they belong to.
    
    Decrepreated in favor of the objected oriented approach
    """
    normalized = [normalize_answer(v) for v in values]
    axis_name, axis_labels, unmatched = detect_axis(values)

    if axis_name in {"unknown", "ambiguous"}:
        # Keep plotting possible, but preserve observed order deterministically
        observed = sorted({v for v in normalized if v is not None})
        counts = pd.Series(normalized).value_counts().reindex(observed, fill_value=0)
        return counts, axis_name, unmatched

    counts = pd.Series(normalized).value_counts().reindex(axis_labels, fill_value=0)
    return counts, axis_name, unmatched




