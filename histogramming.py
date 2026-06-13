



"""
decrepated
"""
# from __main__ import sanitize_key, figure_folder
from matplotlib.pyplot import subplots, show, close
import pandas as pd

from axes import normalize_answer, detect_axis


global data_folder, figure_folder
data_folder = "BaseGeo_2_0\\all data exel"
figure_folder = "BaseGeo_2_0\\figures"



def sanitize_key(key):
    bad_chars = [
        "?", "/", "."
    ]
    for bad_char in bad_chars:
        key = key.replace(bad_char, "")
    return key


def extract_counts(values):
    normalized = [normalize_answer(v) for v in values]
    axis_name, axis, unmatched, coverage = detect_axis(values)

    # fallback: if too little matches, use only observed labels (sorted)
    if axis is None or coverage < 0.5:
        observed = sorted({v for v in normalized if v is not None})
        counts = pd.Series(normalized).value_counts().reindex(observed, fill_value=0)
        return counts, "unknown", unmatched, coverage

    counts = pd.Series(normalized).value_counts().reindex(axis, fill_value=0)
    return counts, axis_name, unmatched, coverage

def make_raw_histograms(data, folder, *args, quiet=False, use_only_known_axes=True, **kwargs):

    # key is the column name, value is the column data
    for key in data.keys():
        
        if not quiet: print(f"{key = }")

        axis_name, axis_or_labels, unmatched = detect_axis(data[key].tolist())
        if axis_name == "unknown":
            counts = pd.Series([normalize_answer(v) for v in data[key]]).value_counts().reindex(axis_or_labels, fill_value=0)
            if use_only_known_axes: continue
        
        counts = pd.Series([normalize_answer(v) for v in data[key]]).value_counts().reindex(axis_or_labels, fill_value=0)
        fig, ax = subplots(figsize=(10, 10))
        ax.bar(counts.index, counts.values)
        ax.set_title(sanitize_key(key))
        ax.tick_params(axis="x", labelrotation=45)

        fig.tight_layout()
        fig.savefig(folder + "\\" + f"{sanitize_key(key)}.png")
        close()
