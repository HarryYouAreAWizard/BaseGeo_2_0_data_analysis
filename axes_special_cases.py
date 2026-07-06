#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""some axes end up not getting an axis because they coincidencially does not have any responses 
that uniquely identifies the axis

following is a dictionary where with predefined axes"""

from axes_container import *

predefined_axes = {
    '2019data\\uibgeophys_2019_students.xlsx': {
        "Fieldwork skills.1": ("extent", AXES_extent["extent"])
    },
    '..\\2019data\\uibgeophys_2019_students.xlsx': {
        "Fieldwork skills.1": ("extent", AXES_extent["extent"])
    },
    '..\\2026data\\data_2026_students.xlsx': {
        'How satisfied are you with the study environment?' : ("nolabels", AXES_nolabels["nolabels"]),
    } 
}