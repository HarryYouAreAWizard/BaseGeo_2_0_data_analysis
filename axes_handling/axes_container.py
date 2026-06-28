#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File: axes_container.py
Author: Noah Nielsen
Created: 2026-06-14
Description: Containers for the various axes used in the survey questions.
"""

AXES_frequencies = {

    "frequency": [
        "1. Never",
        "2.",
        "3.",
        "4. Sometimes",
        "5.",
        "6.",
        "7. Continuously",
    ],
    "frequency_verbose_with_typo": [
        "1. Never",
        "2. Very rerely",
        "3. Rerely",
        "4. Sometimes",
        "5. Often",
        "6. Very often",
        "7. Continuously",
    ],
}

AXES_agreements = {
    "agreement": [
        "1. Strongly disagree",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Strongly agree",
    ],
        "agreement_verbose": [
        "1. Strongly disagree",
        "2. Disagree",
        "3. Slightly disagree",
        "4. Neutral",
        "5. Slightly agree",
        "6. Agree",
        "7. Strongly agree",
    ],
    "agreement_with_doubt": [
        "1. Strongly disagree",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Strongly agree",
        "I don&#39;t know"
    ],
    'agreement_with_different_doubt': [
        '1. Strongly disagree', 
        '2.', 
        '3.', 
        '4. Neutral', 
        '5.', 
        '6.', 
        '7. Strongly agree', 
        'I don&#39;t know'
    ],
    "agreement_not_applicable": [
        "1. Strongly disagree",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Strongly agree",
        "Not applicable"
    ],
    'agreement_clean_with_typo': [
        '1. Stongly disagree', 
        '2.', 
        '3.', 
        '4. Neutral', 
        '5.', 
        '6.', 
        '7. Strongly agree'
    ]
}

AXES_importance = {
    "importance": [
        "1. Not important",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Extremely important"
    ],
    "importance_not_applicable": [
        "1. Not important",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Extremely important",
        "Not applicable"
    ],
    "importance_with_doubt": [
        "1. Not important",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Extremely important",
        "I don&#39;t know"
    ]
}

AXES_extent = {
    "extent": [
        "1. Extremely little",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Extremely well",
    ],
    "extent_with_doubt": [
        "1. Extremely little", 
        "2.", 
        "3.", 
        "4. Neutral", 
        "5.", 
        "6.", 
        "7. Extremely well", 
        "I don&#39;t know"
    ],
    "extent_with_clean_doubt": [
        "1. Extremely little",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Extremely well",
        "I don't know"
    ],
    "extent_with_yet_another_doubt": [
        "1. Extremely little",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Extremely well",
        "I don't know"
    ],
    "extent_with_2_typos": [
        "1. Extremenly little",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Extremely welll",
        "I don't know"
    ],
    "extent_with_1_typo": [
        "1. Extremely little",
        "2.",
        "3.",
        "4. Neutral",
        "5.",
        "6.",
        "7. Extremely welll",
        "I don't know"
    ]
}

AXES_occurence_reverse = {
    "occurence_reverse": [
        "1. Very often",
        "2.",
        "3.",
        "4.",
        "5.",
        "6.",
        "7. Very rarely"
    ]
}

AXES_nolabels = {
    "nolabels": [
        "1.",
        "2.",
        "3.",
        "4.",
        "5.",
        "6.",
        "7."
    ]
}

AXES = {
    "frequency": AXES_frequencies,
    "agreement": AXES_agreements,
    "importance": AXES_importance,
    "extent": AXES_extent,
    "occurence_reverse": AXES_occurence_reverse,
    "nolabels": AXES_nolabels

}