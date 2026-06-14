
import pandas as pd
import re


FREQUENCY_AXIS = [
    "1. Never",
    "2. Very rerely",
    "3. Rerely",
    "4. Sometimes",
    "5. Often",
    "6. Very often",
    "7. Continuously",
    "Not applicable",
]

AGREEMENT_AXIS = [
    "1. Strongly disagree",
    "2. Disagree",
    "3. Slightly disagree",
    "4. Neutral",
    "5. Slightly agree",
    "6. Agree",
    "7. Strongly agree",
    "Not applicable",
]

EXTENT_AXIS = [
    "1. Extremely little",
    "2.",
    "3.",
    "4. Neutral",
    "5.",
    "6.",
    "7. Extremely well",
    "No idea",
]

AXIS_DEFINITIONS = [
    ("frequency", FREQUENCY_AXIS, ["never", "often", "continuously", "very often", "rerely", "sometimes"]),
    ("agreement", AGREEMENT_AXIS, ["strongly disagree", "disagree", "slightly disagree", "slightly agree", "strongly agree", "agree"]),
    ("extent", EXTENT_AXIS, ["extremely little", "extremely well", "no idea"]),
]



def normalize_answer(value):
    if pd.isna(value):
        return None
    
    text = str(value).strip()

    return text



def detect_axis(values):
    labels = {normalize_answer(v) for v in values}
    labels.discard(None)

    best_name = None
    best_axis = None
    best_score = -1

    for axis_name, axis, clues in AXIS_DEFINITIONS:
        axis_set = set(axis)
        exact_hits = sum(1 for label in labels if label in axis_set)

        lowered_labels = [str(label).lower() for label in labels]
        clue_hits = 0
        for clue in clues:
            clue_hits += sum(1 for label in lowered_labels if clue in label)

        bare_number_hits = sum(1 for label in labels if re.match(r"^\d+\.$", str(label)))
        if axis_name == "extent":
            clue_hits += bare_number_hits

        score = exact_hits * 10 + clue_hits

        if score > best_score:
            best_score = score
            best_name = axis_name
            best_axis = axis

    if best_axis is None:
        return None, None, sorted(labels), 0.0

    axis_set = set(best_axis)
    matched = {label for label in labels if label in axis_set}
    unmatched = sorted(label for label in labels if label not in axis_set)

    coverage = len(matched) / len(labels) if labels else 1.0
    return best_name, best_axis, unmatched, coverage
