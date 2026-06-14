

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
    Returns the axis name, the labels for that axis, and any unmatched labels.
     - If exactly one axis matches, returns that axis and its labels.
     - If no axes match, returns "unknown" and the unique normalized labels.
     - If multiple axes match (should not happen if axes are disjoint), returns "ambiguous".
    """
    # clean and normalize the input values to get a set of unique labels
    labels = {normalize_answer(v) for v in values}
    labels.discard(None)

    # check which axes match the labels
    # matches = []
    for axis_name in AXES.keys():
        for axis_variation, axis_labels in AXES[axis_name].items():
            allowed = set(axis_labels) or set(UNIVERSAL_OPTIONS)
            if labels.issubset(allowed):
                axis = axis_name, AXES[axis_name][axis_name] # pick clean version
                return axis
            # try comparing with the first choice in the axis
            if axis_labels[0] in labels:
                axis = axis_name, AXES[axis_name][axis_name] # pick clean version
                return axis
            # try comparing it with the last choice in the clean version of the axis
            if AXES[axis_name][axis_name][-1] in labels:
                axis = axis_name, AXES[axis_name][axis_name] # pick clean version
                return axis

    return None, None


    # if exactly one axis matches, return it with its labels (including any universal options that are present)
    if len(matches) >= 1:
        name = matches[0]
        plot_axis = AXES[name]# + [opt for opt in UNIVERSAL_OPTIONS if opt in labels]
        return name, plot_axis

    # if no axes match, return "unknown" with the unique labels (sorted for consistency)
    if len(matches) == 0:
        return "unknown", sorted(labels) #, sorted(labels)

    # len(matches) > 1: this should not happen if axes are truly disjoint
    # return "ambiguous", sorted(labels) #, sorted(labels)


def extract_counts(values):
    """
    Given a list of raw values, normalize them and detect which axis they belong to.
    
    Decrepreated in favor of objected oriented approach
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




